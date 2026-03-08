"""
DST Speech Ceviri - Gemini 2.5 Flash ile Karakter Konusmalari
==============================================================
OpenRouter uzerinden Gemini 2.5 Flash kullanarak
60,000+ karakter konusma stringini Turkceye cevirir.

Kullanim:
    python tools/translate/translate_speech.py
    python tools/translate/translate_speech.py --api-key sk-or-...
    python tools/translate/translate_speech.py --batch-size 30

Gereksinimler:
    pip install requests
"""

import json
import os
import sys
import time
import re
import argparse
import requests

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JSON_DIR = os.path.join(PROJECT_ROOT, "data", "json")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.5-flash"

BATCH_SIZE = 30
DELAY_BETWEEN = 1.0
MAX_RETRIES = 3
SAVE_EVERY = 5  # Her N batch'te kaydet

SYSTEM_PROMPT = """Sen Don't Starve Together oyunu icin profesyonel bir Turkce cevirmensin.
Karakter konusmalarini (speech) ceviriyorsun.

KURALLAR:
1. Karakter isimleri (Wilson, Willow, Maxwell, Wendy, Wolfgang, WX-78, Wickerbottom, Woodie, Wes, Webber, Wigfrid, Winona, Warly, Wormwood, Wurt, Walter, Wanda, Abigail, Chester, Lucy, Glommer, Charlie) CEVRILMEZ.
2. Oyun esya/yaratik isimleri icin sozlukteki terimleri kullan.
3. Oyunun karanlik mizah tonunu koru.
4. Kisa ve oz ceviriler yap - uzatma.
5. \\n gibi ozel karakterleri aynen koru.
6. Bos string gelirse bos dondur.
7. "only_used_by" gibi meta-stringler varsa aynen birak.
8. Koseli parantez icindeki BAGLAM bilgisi ceviriyi ANLAMLANDIRMAK icindir, ceviriye dahil etme.
   Ornek: [DESCRIBE.AXE] "It's pointy!" -> Karakter baltayi inceliyor, "Sivri!" diye cevir.
   [DESCRIBE.WALLS_WOOD] "Pointy!" -> Karakter ahsap duvari inceliyor, "Sivri!" diye cevir.
9. Her karakter farkli konusur:
   - Wilson (GENERIC): Bilimsel, merakli
   - Willow (WILLOW): Asi, ates takintili
   - Wolfgang (WOLFGANG): Basit, guclu adam konusmasi
   - WX-78 (WX78): Robotik, BUYUK HARFLE konusur
   - Wendy (WENDY): Melankolik, siirsel
   - Wickerbottom (WICKERBOTTOM): Akademik, resmi
   - Woodie (WOODIE): Kanadalı, kibar
   - Webber (WEBBER): Cocuksu, "biz" diye konusur
   - Wathgrithr/Wigfrid (WATHGRITHR): Viking, dramatik
   - Wortox (WORTOX): Seytan, kafiyeli/siirsel
   - Wormwood (WORMWOOD): Bitki-insan, basit
   - Wurt (WURT): Merm, basit konusma

FORMAT: Sana numarali bir liste gelecek. Her satirda [BAGLAM.YOLU] ve ardindan Ingilizce metin var.
Yanit olarak SADECE bir JSON objesi dondur.
JSON'da key'ler "1", "2", "3" gibi numaralar, value'lar Turkce ceviriler olacak.
Ornek: {"1": "Bu guzel bir agac.", "2": "Karnım acıktı.", "3": "Bu ne işe yarar?"}"""


def extract_json_from_text(text):
    """Yanit metninden JSON objesini cikar."""
    text = text.strip()

    # ```json ... ```
    m = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass

    # ``` ... ```
    m = re.search(r'```\s*(.*?)\s*```', text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass

    # { ... }
    first = text.find('{')
    last = text.rfind('}')
    if first != -1 and last > first:
        try:
            return json.loads(text[first:last + 1])
        except json.JSONDecodeError:
            # Trailing comma duzelt
            cleaned = re.sub(r',\s*}', '}', text[first:last + 1])
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                pass

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    return None


def call_api(api_key, user_prompt, glossary_text):
    """OpenRouter API cagrisi."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/dst-turkish-translation",
    }

    system = SYSTEM_PROMPT
    if glossary_text:
        system += f"\n\nSOZLUK (bu terimleri kullan):\n{glossary_text}"

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 8192,
        "response_format": {"type": "json_object"},
    }

    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=180)

            if resp.status_code == 401:
                raise SystemExit("\n  [FATAL] Gecersiz API anahtari (401).")
            if resp.status_code == 403:
                raise SystemExit("\n  [FATAL] API limiti asildi (403). Limit artirin: https://openrouter.ai/settings/keys")
            if resp.status_code == 429:
                wait = DELAY_BETWEEN * (attempt + 3)
                print(f" [rate limit, {wait:.0f}s]", end="", flush=True)
                time.sleep(wait)
                continue

            resp.raise_for_status()
            data = resp.json()

            if "error" in data:
                print(f" [API hata: {str(data['error'])[:80]}]", end="", flush=True)
                if attempt < MAX_RETRIES - 1:
                    time.sleep(DELAY_BETWEEN)
                continue

            choices = data.get("choices", [])
            if not choices:
                print(f" [bos yanit]", end="", flush=True)
                if attempt < MAX_RETRIES - 1:
                    time.sleep(DELAY_BETWEEN)
                continue

            text = choices[0].get("message", {}).get("content", "").strip()
            if not text:
                print(f" [bos icerik]", end="", flush=True)
                if attempt < MAX_RETRIES - 1:
                    time.sleep(DELAY_BETWEEN)
                continue

            result = extract_json_from_text(text)
            if result and isinstance(result, dict):
                return result

            print(f" [JSON parse hata]", end="", flush=True)
            if attempt < MAX_RETRIES - 1:
                time.sleep(DELAY_BETWEEN)

        except SystemExit:
            raise
        except requests.exceptions.RequestException as e:
            print(f" [baglanti: {e}]", end="", flush=True)
            if attempt < MAX_RETRIES - 1:
                time.sleep(DELAY_BETWEEN * 2)
        except Exception as e:
            print(f" [{type(e).__name__}: {e}]", end="", flush=True)
            if attempt < MAX_RETRIES - 1:
                time.sleep(DELAY_BETWEEN)

    return None


def main():
    parser = argparse.ArgumentParser(description="DST Speech Ceviri")
    parser.add_argument("--api-key", default="")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    parser.add_argument("--character", default="", help="Sadece belirli karakter (orn: GENERIC, WAXWELL)")
    parser.add_argument("--fresh", action="store_true", help="Mevcut cevirileri sil, sifirdan basla")
    args = parser.parse_args()

    print()
    print("=" * 60)
    print("  DST SPEECH CEVIRI - Gemini 2.5 Flash")
    print("  OpenRouter uzerinden karakter konusmalari cevirisi")
    print("=" * 60)

    # API key
    api_key = args.api_key or os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        print("\n  OpenRouter API anahtarinizi girin.")
        print("  (https://openrouter.ai/keys)")
        api_key = input("\n  API Anahtari: ").strip()
        if not api_key:
            print("  [HATA] API anahtari gerekli.")
            sys.exit(1)

    # Dosyalari yukle
    speech_en_path = os.path.join(JSON_DIR, "speech_en.json")
    speech_tr_path = os.path.join(JSON_DIR, "speech_tr.json")

    if not os.path.isfile(speech_en_path):
        print(f"\n  [HATA] {speech_en_path} bulunamadi.")
        print("  Once tools/extract/extract_speech.py calistirin.")
        sys.exit(1)

    with open(speech_en_path, "r", encoding="utf-8") as f:
        speech_en = json.load(f)

    speech_tr = {}
    if args.fresh:
        print("\n  [!] --fresh: Mevcut ceviriler sifirlanacak!")
    elif os.path.isfile(speech_tr_path):
        with open(speech_tr_path, "r", encoding="utf-8") as f:
            speech_tr = json.load(f)

    # Glossary yukle
    glossary_path = os.path.join(JSON_DIR, "glossary.json")
    glossary_text = ""
    if os.path.isfile(glossary_path):
        with open(glossary_path, "r", encoding="utf-8") as f:
            glossary = json.load(f)
        # En onemli 150 terimi al (prompt boyutunu sinirla)
        important = dict(sorted(glossary.items())[:150])
        glossary_text = json.dumps(important, ensure_ascii=False)
        print(f"\n  Sozluk yuklendi: {len(glossary)} terim (prompt'a {len(important)} eklendi)")

    # Cevrilmemis stringleri bul
    to_translate = {}
    for key, value in speech_en.items():
        if not value or not value.strip():
            continue
        if args.character and not key.startswith(f"CHARACTERS.{args.character}."):
            continue
        if key not in speech_tr or not speech_tr[key]:
            to_translate[key] = value

    total_en = len(speech_en)
    already_done = len(speech_tr)
    remaining = len(to_translate)

    print(f"\n  Toplam speech string:  {total_en:,}")
    print(f"  Zaten cevrilmis:       {already_done:,}")
    print(f"  Cevrilecek:            {remaining:,}")

    if remaining == 0:
        print("\n  Tum speech stringler cevrilmis!")
        return

    # Maliyet tahmini
    avg_chars = sum(len(v) for v in to_translate.values()) / max(remaining, 1)
    est_input_tokens = remaining * (avg_chars / 3.5 + 15)  # string + overhead
    est_output_tokens = remaining * (avg_chars * 1.2 / 3.5)
    est_cost = (est_input_tokens * 0.30 + est_output_tokens * 2.50) / 1_000_000
    print(f"  Tahmini maliyet:       ~${est_cost:.2f}")

    batch_size = args.batch_size
    keys_list = list(to_translate.keys())
    total_batches = (remaining + batch_size - 1) // batch_size
    translated_count = 0
    error_count = 0

    print(f"\n  Batch boyutu: {batch_size} | Toplam batch: {total_batches:,}")
    print(f"  Model: {MODEL}")
    print()

    # Baglanti testi
    print("  Baglanti test ediliyor...", end="", flush=True)
    try:
        resp = requests.post(OPENROUTER_URL, headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }, json={
            "model": MODEL,
            "messages": [{"role": "user", "content": "Say OK"}],
            "max_tokens": 10,
        }, timeout=15)
        if resp.status_code == 200:
            print(" OK!")
        else:
            print(f" HATA ({resp.status_code})")
            print(f"  {resp.text[:200]}")
            sys.exit(1)
    except Exception as e:
        print(f" HATA: {e}")
        sys.exit(1)

    print()
    start_time = time.time()

    try:
        for i in range(0, len(keys_list), batch_size):
            batch_keys = keys_list[i:i + batch_size]
            batch_num = i // batch_size + 1

            # Ilerleme yuzdesi
            pct = (i / remaining) * 100
            elapsed = time.time() - start_time
            if translated_count > 0:
                eta = (elapsed / translated_count) * (remaining - translated_count)
                eta_str = f" ETA:{eta/60:.0f}dk"
            else:
                eta_str = ""

            print(f"  [{batch_num:,}/{total_batches:,}] %{pct:.1f}{eta_str} ...", end="", flush=True)

            # Numarali liste olustur - KEY bilgisi baglam olarak eklenir
            lines = []
            for idx, key in enumerate(batch_keys, 1):
                # CHARACTERS.GENERIC.DESCRIBE.AXE -> [DESCRIBE.AXE]
                # Key'den karakter prefix'ini cikar, geri kalani baglam olarak ekle
                parts = key.split(".", 2)  # CHARACTERS, CHARNAME, geri_kalan
                context = parts[2] if len(parts) > 2 else key
                lines.append(f"{idx}. [{context}] {to_translate[key]}")
            numbered_list = "\n".join(lines)

            prompt = f"""Asagidaki {len(batch_keys)} Don't Starve Together karakter konusmasini Turkceye cevir.
Koseli parantez icindeki kisim BAGLAM bilgisidir (esya/yaratik/durum), ceviriye dahil etme.

{numbered_list}

SADECE JSON dondur: {{"1": "ceviri", "2": "ceviri", ...}}"""

            result = call_api(api_key, prompt, glossary_text)
            if result:
                matched = 0
                for idx, key in enumerate(batch_keys, 1):
                    str_idx = str(idx)
                    if str_idx in result and isinstance(result[str_idx], str) and result[str_idx].strip():
                        speech_tr[key] = result[str_idx]
                        translated_count += 1
                        matched += 1
                print(f" +{matched}")
            else:
                error_count += 1
                print(f" HATA")

            # Periyodik kayit
            if batch_num % SAVE_EVERY == 0:
                with open(speech_tr_path, "w", encoding="utf-8") as f:
                    json.dump(speech_tr, f, ensure_ascii=False, indent=2, sort_keys=True)
                done_pct = len(speech_tr) * 100 / total_en
                print(f"  >>> Kaydedildi: {len(speech_tr):,}/{total_en:,} (%{done_pct:.1f})")

            time.sleep(DELAY_BETWEEN)

    except (KeyboardInterrupt, SystemExit) as e:
        print(f"\n\n  Durduruluyor... Ilerleme kaydediliyor...")
        with open(speech_tr_path, "w", encoding="utf-8") as f:
            json.dump(speech_tr, f, ensure_ascii=False, indent=2, sort_keys=True)
        print(f"  Kaydedildi: {len(speech_tr):,} ceviri")
        if isinstance(e, SystemExit):
            raise
        sys.exit(0)

    # Son kayit
    with open(speech_tr_path, "w", encoding="utf-8") as f:
        json.dump(speech_tr, f, ensure_ascii=False, indent=2, sort_keys=True)

    elapsed = time.time() - start_time
    final_pct = len(speech_tr) * 100 / total_en

    print()
    print("=" * 60)
    print(f"  TAMAMLANDI!")
    print(f"  Yeni ceviri:    {translated_count:,}")
    print(f"  Toplam ceviri:  {len(speech_tr):,}/{total_en:,} (%{final_pct:.1f})")
    print(f"  Hatali batch:   {error_count}")
    print(f"  Sure:           {elapsed/60:.1f} dakika")
    print(f"  Kayit:          {speech_tr_path}")
    print("=" * 60)

    if error_count > 0:
        print(f"\n  {error_count} batch basarisiz oldu. Scripti tekrar calistirarak")
        print(f"  kaldiginiz yerden devam edebilirsiniz.")


if __name__ == "__main__":
    main()
