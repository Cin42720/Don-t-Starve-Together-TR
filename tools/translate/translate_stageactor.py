"""
DST StageActor Ceviri - Gemini 2.5 Flash ile Sahne Performanslari
==================================================================
OpenRouter uzerinden Gemini 2.5 Flash kullanarak
592 sahne performansi stringini Turkceye cevirir.

Kullanim:
    python tools/translate/translate_stageactor.py
    python tools/translate/translate_stageactor.py --api-key sk-or-...
    python tools/translate/translate_stageactor.py --batch-size 20

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

BATCH_SIZE = 20
DELAY_BETWEEN = 1.0
MAX_RETRIES = 3
SAVE_EVERY = 5

SYSTEM_PROMPT = """Sen Don't Starve Together oyunu icin profesyonel bir Turkce cevirmensin.
Sahne performansi (stage actor) diyaloglarini ceviriyorsun. Bunlar oyundaki NPC'lerin
sahnede sergiledigi tiyatro oyunlari, monologlar ve siirlerdir.

KURALLAR:
1. Karakter isimleri (Wilson, Willow, Maxwell, Wendy, Wolfgang, WX-78, Wickerbottom, Woodie, Wes, Webber, Wigfrid, Winona, Warly, Wormwood, Wurt, Walter, Wanda, Abigail, Chester, Lucy, Glommer, Charlie) CEVRILMEZ.
2. Oyunun karanlik ve gotik atmosferini koru.
3. Tiyatro/sahne dili kullan - edebi ve dramatik bir ton.
4. \\n gibi ozel karakterleri aynen koru.
5. Siirsel yapiyi ve kafiyeleri mumkun oldugu kadar Turkceye uyarla.
6. Bos string gelirse bos dondur.
7. Oyun icindeki yer/esya isimleri icin sozlukteki terimleri kullan.
8. ACT/SCENE yapilarinda tiyatro dili kullan (Perde, Sahne).
9. SOLILOQUY diyaloglari karakter monologlaridir - karakterin kisiligini yansit.
10. THEVAULT ve THEVEIL antik/gizemli hikayelerdir - mistik bir ton kullan.
11. Wes'in diyaloglari Fransizca olabilir - Fransizca birak veya baska bir dilde cevirme.
12. Wormwood'un diyaloglari ses efektleri olabilir - aynen birak.

FORMAT: Sana numarali bir liste gelecek. Her satirda [KATEGORI] ve ardindan Ingilizce metin var.
Yanit olarak SADECE bir JSON objesi dondur.
JSON'da key'ler "1", "2", "3" gibi numaralar, value'lar Turkce ceviriler olacak.
Ornek: {"1": "Ah, ne hazin bir kader!", "2": "Karanlik cokerken...", "3": "Dinleyin!"}"""


def extract_json_from_text(text):
    """Yanit metninden JSON objesini cikar."""
    text = text.strip()

    m = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass

    m = re.search(r'```\s*(.*?)\s*```', text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass

    first = text.find('{')
    last = text.rfind('}')
    if first != -1 and last > first:
        try:
            return json.loads(text[first:last + 1])
        except json.JSONDecodeError:
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
                raise SystemExit("\n  [FATAL] API limiti asildi (403).")
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


# Cevirilmemesi gereken kategoriler
SKIP_CATEGORIES = {
    "WES1",       # Fransizca diyaloglar - aynen kalmali
    "WORMWOOD1",  # Ses efektleri - aynen kalmali
}


def main():
    parser = argparse.ArgumentParser(description="DST StageActor Ceviri")
    parser.add_argument("--api-key", default="")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    parser.add_argument("--fresh", action="store_true", help="Mevcut cevirileri sil, sifirdan basla")
    args = parser.parse_args()

    print()
    print("=" * 60)
    print("  DST STAGEACTOR CEVIRI - Gemini 2.5 Flash")
    print("  Sahne performansi diyaloglari cevirisi")
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
    en_path = os.path.join(JSON_DIR, "stageactor_en.json")
    tr_path = os.path.join(JSON_DIR, "stageactor_tr.json")

    if not os.path.isfile(en_path):
        print(f"\n  [HATA] {en_path} bulunamadi.")
        print("  Once tools/extract/extract_stageactor.py calistirin.")
        sys.exit(1)

    with open(en_path, "r", encoding="utf-8") as f:
        stageactor_en = json.load(f)

    stageactor_tr = {}
    if args.fresh:
        print("\n  [!] --fresh: Mevcut ceviriler sifirlanacak!")
    elif os.path.isfile(tr_path):
        with open(tr_path, "r", encoding="utf-8") as f:
            stageactor_tr = json.load(f)

    # Glossary yukle
    glossary_path = os.path.join(JSON_DIR, "glossary.json")
    glossary_text = ""
    if os.path.isfile(glossary_path):
        with open(glossary_path, "r", encoding="utf-8") as f:
            glossary = json.load(f)
        important = dict(sorted(glossary.items())[:100])
        glossary_text = json.dumps(important, ensure_ascii=False)
        print(f"\n  Sozluk yuklendi: {len(glossary)} terim")

    # Atlanacak stringleri belirle ve cevirilmemisleri bul
    to_translate = {}
    skipped = 0
    for key, value in stageactor_en.items():
        if not value or not value.strip():
            continue
        cat = key.split('.')[0]
        if cat in SKIP_CATEGORIES:
            # Atla ama orjinalini kopyala
            if key not in stageactor_tr:
                stageactor_tr[key] = value
            skipped += 1
            continue
        if key not in stageactor_tr or not stageactor_tr[key]:
            to_translate[key] = value

    total_en = len(stageactor_en)
    already_done = sum(1 for k in stageactor_en if k in stageactor_tr and stageactor_tr[k])
    remaining = len(to_translate)

    print(f"\n  Toplam stageactor string:  {total_en:,}")
    print(f"  Zaten cevrilmis:           {already_done:,}")
    print(f"  Atlanan (WES/WORMWOOD):    {skipped}")
    print(f"  Cevrilecek:                {remaining:,}")

    if remaining == 0:
        print("\n  Tum stageactor stringler cevrilmis!")
        # Yine de kaydet (atlananlari eklemis olabiliriz)
        with open(tr_path, "w", encoding="utf-8") as f:
            json.dump(stageactor_tr, f, ensure_ascii=False, indent=2, sort_keys=True)
        return

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

            pct = (i / remaining) * 100
            elapsed = time.time() - start_time
            if translated_count > 0:
                eta = (elapsed / translated_count) * (remaining - translated_count)
                eta_str = f" ETA:{eta/60:.0f}dk"
            else:
                eta_str = ""

            print(f"  [{batch_num:,}/{total_batches:,}] %{pct:.1f}{eta_str} ...", end="", flush=True)

            lines = []
            for idx, key in enumerate(batch_keys, 1):
                cat = key.split('.')[0]
                lines.append(f"{idx}. [{cat}] {to_translate[key]}")
            numbered_list = "\n".join(lines)

            prompt = f"""Asagidaki {len(batch_keys)} Don't Starve Together sahne performansi diyalogunu Turkceye cevir.
Koseli parantez icindeki kisim KATEGORI bilgisidir (tiyatro perde/sahne veya karakter monologu).
ACT/SCENE = Tiyatro oyunu diyaloglari, SOLILOQUY = Karakter monologlari, THEVAULT/THEVEIL = Antik hikayeler.

{numbered_list}

SADECE JSON dondur: {{"1": "ceviri", "2": "ceviri", ...}}"""

            result = call_api(api_key, prompt, glossary_text)
            if result:
                matched = 0
                for idx, key in enumerate(batch_keys, 1):
                    str_idx = str(idx)
                    if str_idx in result and isinstance(result[str_idx], str) and result[str_idx].strip():
                        stageactor_tr[key] = result[str_idx]
                        translated_count += 1
                        matched += 1
                print(f" +{matched}")
            else:
                error_count += 1
                print(f" HATA")

            if batch_num % SAVE_EVERY == 0:
                with open(tr_path, "w", encoding="utf-8") as f:
                    json.dump(stageactor_tr, f, ensure_ascii=False, indent=2, sort_keys=True)
                done_pct = len(stageactor_tr) * 100 / total_en
                print(f"  >>> Kaydedildi: {len(stageactor_tr):,}/{total_en:,} (%{done_pct:.1f})")

            time.sleep(DELAY_BETWEEN)

    except (KeyboardInterrupt, SystemExit) as e:
        print(f"\n\n  Durduruluyor... Ilerleme kaydediliyor...")
        with open(tr_path, "w", encoding="utf-8") as f:
            json.dump(stageactor_tr, f, ensure_ascii=False, indent=2, sort_keys=True)
        print(f"  Kaydedildi: {len(stageactor_tr):,} ceviri")
        if isinstance(e, SystemExit):
            raise
        sys.exit(0)

    # Son kayit
    with open(tr_path, "w", encoding="utf-8") as f:
        json.dump(stageactor_tr, f, ensure_ascii=False, indent=2, sort_keys=True)

    elapsed = time.time() - start_time
    final_pct = len(stageactor_tr) * 100 / total_en

    print()
    print("=" * 60)
    print(f"  TAMAMLANDI!")
    print(f"  Yeni ceviri:    {translated_count:,}")
    print(f"  Toplam ceviri:  {len(stageactor_tr):,}/{total_en:,} (%{final_pct:.1f})")
    print(f"  Hatali batch:   {error_count}")
    print(f"  Sure:           {elapsed/60:.1f} dakika")
    print(f"  Kayit:          {tr_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
