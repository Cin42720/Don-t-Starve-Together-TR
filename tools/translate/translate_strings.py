"""
DST Pro Çeviri Pipeline - 3 Aşamalı Hibrit AI Çeviri
=======================================================
OpenRouter üzerinden Gemini + Claude kullanarak profesyonel
çeviri pipeline'ı çalıştırır.

Aşama 1 (Gemini): Oyun sözlüğü oluştur (terimler, eşya/yer/karakter isimleri)
Aşama 2 (Claude): Sözlüğe sadık kalarak bağlamsal çeviri yap
Aşama 3 (Gemini): Son kontrol - gramer, tutarlılık, sözlük uyumu

Kullanım:
    python tools/translate/translate_strings.py

Gereksinimler:
    pip install requests

API Anahtarı:
    https://openrouter.ai/keys adresinden alın
"""

import json
import os
import sys
import time
import re
import requests

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JSON_DIR = os.path.join(PROJECT_ROOT, "data", "json")
MOD_DIR = os.path.join(PROJECT_ROOT, "mod")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Model seçimleri
GEMINI_MODEL = "google/gemini-2.0-flash-001"          # Aşama 1: Sözlük (hızlı, ucuz)
CLAUDE_MODEL = "anthropic/claude-sonnet-4"             # Aşama 2: Çeviri (kaliteli)
CLAUDE_OPUS_MODEL = "google/gemini-2.0-flash-001"     # Aşama 3a: Kontrol (varsayılan ucuz)
GEMINI_PRO_MODEL = "google/gemini-2.0-flash-001"      # Aşama 3b: İkinci kontrol (varsayılan ucuz)
# NOT: Kaliteli kontrol için yukarıdaki 3a ve 3b modellerini şu şekilde değiştirin:
#   CLAUDE_OPUS_MODEL = "anthropic/claude-opus-4"
#   GEMINI_PRO_MODEL = "google/gemini-2.5-pro-preview"

# Batch ayarları
BATCH_SIZE = 20         # 30 yanıta sığmıyordu, 20 optimal (~1700 token yanıt)
DELAY_BETWEEN = 1.5
MAX_RETRIES = 3

# ===================== SÖZLÜK PROMPTLARI =====================

GLOSSARY_SYSTEM = """Sen Don't Starve Together oyunu uzmanısın.
Sana oyundaki İngilizce terimleri vereceğim.
Bu terimlerin Türkçe karşılıklarını içeren bir SÖZLÜK oluştur.

Kurallar:
- Karakter isimleri (Wilson, Willow, Maxwell, Webber vb.) ÇEVRİLMEZ.
- Yaratık/eşya/yer isimleri için doğal Türkçe karşılıklar bul.
- Aynı terim her yerde AYNI şekilde çevrilmeli (tutarlılık).
- Oyunun karanlık-mizahi tonuna uygun ol.
- JSON formatında döndür: {"İngilizce": "Türkçe", ...}
"""

TRANSLATE_SYSTEM = """Sen Don't Starve Together oyunu icin profesyonel bir Turkce cevirmensin.

KURALLAR:
1. Sozlukteki terimleri BIREBIR kullan.
2. Karakter isimleri (Wilson, Willow, Maxwell vb.) CEVRILMEZ.
3. Oyunun karanlik mizah tonunu koru.
4. Kisa ve oz ceviriler yap.
5. \\n gibi ozel karakterleri aynen koru.
6. Bos string gelirse bos dondur.

FORMAT: Sana numarali bir liste gelecek. Yanit olarak SADECE bir JSON objesi dondur.
JSON'da key'ler "1", "2", "3" gibi numaralar, value'lar Turkce ceviriler olacak.
Ornek: {"1": "Balta", "2": "Kamp Atesi", "3": "Odun kes"}"""

REVIEW_SYSTEM = """Sen bir Türkçe dil uzmanısın ve Don't Starve Together oyununu iyi biliyorsun.
Sana çevrilmiş oyun metinleri ve kullanılması gereken sözlük verilecek.

Görevin:
1. Sözlüğe AYKIRI çevirileri düzelt (aynı terim farklı çevrilmişse).
2. Türkçe gramer hatalarını düzelt.
3. Doğal olmayan/garip çevirileri iyileştir.
4. Karakter isimleri çevrilmişse düzelt (çevrilmemeli).
5. Çok uzun çevirileri kısalt.

Düzeltilmiş JSON döndür. Değişiklik yoksa aynısını döndür.
SADECE JSON formatında yanıt ver."""


def flatten_dict(d, prefix=""):
    result = {}
    for key, value in d.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            result.update(flatten_dict(value, full_key))
        elif isinstance(value, str):
            result[full_key] = value
    return result


def unflatten_dict(flat):
    result = {}
    for key, value in flat.items():
        keys = key.split(".")
        current = result
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value
    return result


def extract_json_from_text(text):
    """Yanıt metninden JSON objesini çıkar. Birden fazla yöntem dener."""
    text = text.strip()

    # Yöntem 1: ```json ... ``` bloğu
    json_match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    # Yöntem 2: ``` ... ``` bloğu (json etiketi olmadan)
    json_match = re.search(r'```\s*(.*?)\s*```', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    # Yöntem 3: İlk { ile son } arasını al
    first_brace = text.find('{')
    last_brace = text.rfind('}')
    if first_brace != -1 and last_brace > first_brace:
        try:
            return json.loads(text[first_brace:last_brace + 1])
        except json.JSONDecodeError:
            pass

    # Yöntem 4: Trailing comma düzelt ve tekrar dene
    if first_brace != -1 and last_brace > first_brace:
        cleaned = text[first_brace:last_brace + 1]
        cleaned = re.sub(r',\s*}', '}', cleaned)  # ,} → }
        cleaned = re.sub(r',\s*]', ']', cleaned)  # ,] → ]
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

    # Yöntem 5: Direkt parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    return None


def call_openrouter(api_key, model, system_prompt, user_prompt):
    """OpenRouter API çağrısı yap."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/dst-turkish-translation",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 8192,
        "response_format": {"type": "json_object"},
    }

    last_raw_text = ""  # Debug için son yanıtı sakla

    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=180)

            # 403 = limit aşıldı veya yetki yok → tekrar denemenin anlamı yok
            if resp.status_code == 403:
                print(f" [403 DURDURULDU]", end="", flush=True)
                raise SystemExit("\n\n  [FATAL] API limiti aşıldı (403 Forbidden).\n"
                                 "  Limit artırın: https://openrouter.ai/settings/keys\n"
                                 "  İlerleme kaydedildi, kaldığınız yerden devam edebilirsiniz.")

            # 401 = geçersiz anahtar → tekrar denemenin anlamı yok
            if resp.status_code == 401:
                print(f" [401 DURDURULDU]", end="", flush=True)
                raise SystemExit("\n\n  [FATAL] Geçersiz API anahtarı (401).\n"
                                 "  API anahtarınızı kontrol edin.")

            if resp.status_code == 429:
                wait = DELAY_BETWEEN * (attempt + 2)
                print(f" [rate limit, {wait}s]", end="", flush=True)
                time.sleep(wait)
                continue

            resp.raise_for_status()
            data = resp.json()

            # OpenRouter hata mesajı kontrolü
            if "error" in data:
                err_msg = data["error"].get("message", str(data["error"]))
                print(f" [API hata: {err_msg[:80]}]", end="", flush=True)
                if attempt < MAX_RETRIES - 1:
                    time.sleep(DELAY_BETWEEN)
                continue

            # Yanıt yapısını güvenli kontrol et
            choices = data.get("choices", [])
            if not choices:
                # Ham yanıtı debug'a kaydet
                debug_path = os.path.join(JSON_DIR, "debug_last_response.txt")
                with open(debug_path, "w", encoding="utf-8") as f:
                    f.write(f"Model: {model}\n")
                    f.write(f"Zaman: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"{'='*60}\n")
                    f.write(json.dumps(data, ensure_ascii=False, indent=2))
                print(f" [boş yanıt, tekrar {attempt+1}/{MAX_RETRIES}]", end="", flush=True)
                if attempt < MAX_RETRIES - 1:
                    time.sleep(DELAY_BETWEEN)
                continue

            msg = choices[0].get("message", {})
            text = msg.get("content", "")
            if not text:
                print(f" [boş içerik, tekrar {attempt+1}/{MAX_RETRIES}]", end="", flush=True)
                if attempt < MAX_RETRIES - 1:
                    time.sleep(DELAY_BETWEEN)
                continue

            text = text.strip()
            last_raw_text = text

            # Gelişmiş JSON çıkarma
            result = extract_json_from_text(text)
            if result and isinstance(result, dict):
                return result

            print(f" [JSON parse başarısız, tekrar {attempt+1}/{MAX_RETRIES}]", end="", flush=True)
            if attempt < MAX_RETRIES - 1:
                time.sleep(DELAY_BETWEEN)

        except SystemExit:
            raise
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if "403" in error_msg or "Forbidden" in error_msg:
                raise SystemExit("\n\n  [FATAL] API limiti aşıldı (403).\n"
                                 "  Limit artırın: https://openrouter.ai/settings/keys")
            print(f" [bağlantı hatası: {e}]", end="", flush=True)
            if attempt < MAX_RETRIES - 1:
                time.sleep(DELAY_BETWEEN * 2)
        except Exception as e:
            # Beklenmeyen hata (KeyError, IndexError vb.)
            print(f" [hata: {type(e).__name__}: {e}]", end="", flush=True)
            if attempt < MAX_RETRIES - 1:
                time.sleep(DELAY_BETWEEN)

    # Tüm denemeler başarısız - debug bilgisi kaydet
    if last_raw_text:
        debug_path = os.path.join(JSON_DIR, "debug_last_response.txt")
        with open(debug_path, "w", encoding="utf-8") as f:
            f.write(f"Model: {model}\n")
            f.write(f"Zaman: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*60}\n")
            f.write(last_raw_text)
        print(f" [debug: {debug_path}]", end="", flush=True)

    return None


def save_progress(data, path):
    """İlerlemeyi kaydet."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)


# ===================== AŞAMA 1: SÖZLÜK =====================

def phase1_glossary(api_key, en_flat):
    """Gemini ile oyun sözlüğü oluştur."""
    glossary_path = os.path.join(JSON_DIR, "glossary.json")

    # Mevcut sözlük varsa yükle
    if os.path.isfile(glossary_path):
        with open(glossary_path, "r", encoding="utf-8") as f:
            existing = json.load(f)
        print(f"  Mevcut sözlük yüklendi: {len(existing)} terim")
        answer = input("  Sözlüğü yeniden oluşturmak ister misiniz? (e/h): ").strip().lower()
        if answer not in ("e", "evet", "y", "yes"):
            return existing

    print("\n  AŞAMA 1: Gemini ile oyun sözlüğü oluşturuluyor...")
    print("  " + "-" * 50)

    # Benzersiz terimleri topla
    unique_terms = set()
    for key, value in en_flat.items():
        # NAMES kategorisindeki tüm değerler önemli terimler
        if ".NAMES." in key or key.startswith("NAMES."):
            unique_terms.add(value)
        # Diğer kategorilerden de tekrar eden kelimeleri topla
        for word in value.split():
            if len(word) > 3 and word[0].isupper():
                unique_terms.add(word)

    # Karakter isimlerini hariç tut
    character_names = {
        "Wilson", "Willow", "Wendy", "Wolfgang", "Wickerbottom",
        "Woodie", "Wes", "Maxwell", "Wigfrid", "Webber", "Winona",
        "Warly", "Wormwood", "Wurt", "Walter", "Wanda", "WX-78",
        "Abigail", "Charlie", "Lucy", "Chester", "Glommer",
    }
    unique_terms -= character_names

    terms_list = sorted(unique_terms)
    print(f"  {len(terms_list)} benzersiz terim bulundu.")

    # Terimleri batch'lere böl ve çevirt
    glossary = {}
    batch_size = 80

    for i in range(0, len(terms_list), batch_size):
        batch = terms_list[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(terms_list) + batch_size - 1) // batch_size

        print(f"  [{batch_num}/{total_batches}] {len(batch)} terim çevriliyor...", end="", flush=True)

        prompt = f"""Bu Don't Starve Together oyun terimlerini Türkçeye çevir.
JSON formatında döndür: {{"İngilizce": "Türkçe"}}

Terimler:
{json.dumps(batch, ensure_ascii=False)}"""

        result = call_openrouter(api_key, GEMINI_MODEL, GLOSSARY_SYSTEM, prompt)
        if result:
            glossary.update(result)
            print(f" OK (+{len(result)})")
        else:
            print(" HATA")

        time.sleep(DELAY_BETWEEN)

    # Kaydet
    save_progress(glossary, glossary_path)
    print(f"\n  [OK] Sozluk kaydedildi: {len(glossary)} terim -> {glossary_path}")
    return glossary


# ===================== AŞAMA 2: ÇEVİRİ =====================

def phase2_translate(api_key, en_flat, glossary, existing_tr):
    """Claude ile sozluk-tabanli ceviri yap. Numarali liste formati kullanir."""
    print("\n  ASAMA 2: Claude ile baglamsal ceviri yapiliyor...")
    print("  " + "-" * 50)

    # Sozluk ozeti (prompt'a eklenecek)
    glossary_text = json.dumps(glossary, ensure_ascii=False, indent=1)
    if len(glossary_text) > 3000:
        important = {k: v for k, v in sorted(glossary.items())[:200]}
        glossary_text = json.dumps(important, ensure_ascii=False, indent=1)

    # Cevrilmemis stringleri bul
    to_translate = {}
    for key, value in en_flat.items():
        if key not in existing_tr or not existing_tr[key].strip():
            to_translate[key] = value

    if not to_translate:
        print("  Tum stringler zaten cevrilmis!")
        return existing_tr

    tr_flat = dict(existing_tr)
    keys_list = list(to_translate.keys())
    total_batches = (len(keys_list) + BATCH_SIZE - 1) // BATCH_SIZE
    translated_count = 0

    print(f"  {len(to_translate)} string cevrilecek ({total_batches} batch)")

    try:
        for i in range(0, len(keys_list), BATCH_SIZE):
            batch_keys = keys_list[i:i + BATCH_SIZE]
            batch_num = i // BATCH_SIZE + 1

            print(f"  [{batch_num}/{total_batches}] {len(batch_keys)} string...", end="", flush=True)

            # Numarali liste formati olustur
            lines = []
            for idx, key in enumerate(batch_keys, 1):
                en_text = to_translate[key]
                lines.append(f"{idx}. {en_text}")

            numbered_list = "\n".join(lines)

            prompt = f"""SOZLUK:
{glossary_text}

Asagidaki {len(batch_keys)} metni Turkceye cevir.
Her satir bir numara ile basliyor. Ayni numarayla JSON dondur.

{numbered_list}

YANITINI SADECE su formatta ver:
{{"1": "cevirisi", "2": "cevirisi", ...}}"""

            result = call_openrouter(api_key, CLAUDE_MODEL, TRANSLATE_SYSTEM, prompt)
            if result:
                matched = 0
                for idx, key in enumerate(batch_keys, 1):
                    str_idx = str(idx)
                    if str_idx in result and isinstance(result[str_idx], str):
                        tr_flat[key] = result[str_idx]
                        translated_count += 1
                        matched += 1
                print(f" OK (+{matched})")
            else:
                print(" HATA")

            # Her 5 batch'te kaydet
            if batch_num % 5 == 0:
                tr_path = os.path.join(JSON_DIR, "strings_tr.json")
                save_progress(unflatten_dict(tr_flat), tr_path)
                print(f"  [KAYIT] Ilerleme kaydedildi")

            time.sleep(DELAY_BETWEEN)
    except SystemExit as e:
        tr_path = os.path.join(JSON_DIR, "strings_tr.json")
        save_progress(unflatten_dict(tr_flat), tr_path)
        print(f"\n  [KAYIT] Hata oncesi ilerleme kaydedildi ({translated_count} yeni ceviri)")
        raise

    print(f"\n  [OK] {translated_count} string cevrildi (Claude)")
    return tr_flat


# ===================== AŞAMA 3: ÇİFT KONTROL =====================

OPUS_REVIEW_SYSTEM = """Sen üst düzey bir Türkçe dil uzmanı ve Don't Starve Together oyun çevirmensin.

Görevin çevirileri derinlemesine kontrol etmek:

1. SÖZLÜK TUTARLILIĞI: Aynı terim her yerde aynı mı çevrilmiş?
   - Sözlükte "Axe" = "Balta" ise, hiçbir yerde "Keser" olmamalı.
2. GRAMER: Türkçe dilbilgisi hatalarını düzelt.
   - Ek uyumu, büyük/küçük harf, noktalama.
3. DOĞALLIK: Çeviri Türkçe'de doğal mı duyuluyor?
   - Kelime kelime çeviri yerine doğal Türkçe ifadeler kullan.
4. KARAKTER KİŞİLİĞİ: Her karakter kendi tarzında mı konuşuyor?
   - Wilson: bilimsel, meraklı
   - Willow: asi, ateşe takıntılı
   - Wolfgang: basit, güçlü
   - WX-78: robotik, soğuk
   - Wendy: melankolik, şiirsel
   - Wickerbottom: akademik, resmi
5. KARAKTER İSİMLERİ: Wilson, Willow vb. çevrilMEMELİ.
6. UZUNLUK: Oyun UI'ında yer sınırlı, çeviriler kısa olmalı.

Düzeltilmiş JSON döndür. Değişiklik yoksa aynısını döndür.
SADECE JSON formatında yanıt ver."""

GEMINI_PRO_REVIEW_SYSTEM = """Sen profesyonel bir Türkçe editörsün.
Sana oyun çevirileri ve bir terim sözlüğü verilecek.

Son kontrol olarak şunları yap:
1. Yazım hatası var mı? (ş/s, ç/c, ğ/g, ü/u, ö/o, ı/i karışıklığı)
2. Sözlüğe aykırı çeviri var mı?
3. Anlam bozukluğu veya garip ifade var mı?
4. Çevrilmemesi gereken isimler (Wilson, Maxwell vb.) çevrilmiş mi?
5. Çok uzun çeviriler kısaltılabilir mi?

Düzeltilmiş JSON döndür. SADECE JSON formatında yanıt ver."""


def _run_review_pass(api_key, model, system_prompt, tr_flat, glossary, pass_name):
    """Tek bir kontrol geçişi çalıştır."""
    glossary_text = json.dumps(glossary, ensure_ascii=False, indent=1)
    if len(glossary_text) > 3000:
        important = {k: v for k, v in sorted(glossary.items())[:200]}
        glossary_text = json.dumps(important, ensure_ascii=False, indent=1)

    translated = {k: v for k, v in tr_flat.items() if v.strip()}
    keys_list = list(translated.keys())
    review_batch_size = 40
    total_batches = (len(keys_list) + review_batch_size - 1) // review_batch_size
    fixed_count = 0

    print(f"  {len(translated)} çeviri kontrol edilecek ({total_batches} batch)")

    try:
        for i in range(0, len(keys_list), review_batch_size):
            batch_keys = keys_list[i:i + review_batch_size]
            batch_num = i // review_batch_size + 1
            batch_dict = {k: translated[k] for k in batch_keys}

            print(f"  [{batch_num}/{total_batches}] {len(batch_keys)} çeviri...", end="", flush=True)

            prompt = f"""SÖZLÜK (terimlere uygunluk kontrol et):
{glossary_text}

Aşağıdaki Türkçe çevirileri kontrol et ve gerekirse düzelt.
Düzeltme yoksa aynısını döndür. SADECE JSON döndür.

```json
{json.dumps(batch_dict, ensure_ascii=False, indent=2)}
```"""

            result = call_openrouter(api_key, model, system_prompt, prompt)
            if result:
                for key in batch_keys:
                    if key in result and result[key] != tr_flat.get(key):
                        tr_flat[key] = result[key]
                        fixed_count += 1
                print(f" OK")
            else:
                print(" HATA")

            time.sleep(DELAY_BETWEEN)
    except SystemExit as e:
        # 403/401 hatası - ilerlemeyi kaydet ve çık
        tr_path = os.path.join(JSON_DIR, "strings_tr.json")
        save_progress(unflatten_dict(tr_flat), tr_path)
        print(f"\n  [KAYIT] Kontrol ilerleme kaydedildi ({fixed_count} düzeltme)")
        raise

    print(f"  [{pass_name}] {fixed_count} düzeltme yapıldı")
    return tr_flat, fixed_count


def phase3_review(api_key, tr_flat, glossary):
    """Çift geçişli kalite kontrol: Claude Opus → Gemini Pro."""
    print("\n  AŞAMA 3: ÇİFT KALİTE KONTROL")
    print("  " + "-" * 50)

    # Geçiş 1: Claude Opus - derin analiz
    print("\n  [3a] Claude Opus 4 - Derin dil ve bağlam kontrolü")
    tr_flat, opus_fixes = _run_review_pass(
        api_key, CLAUDE_OPUS_MODEL, OPUS_REVIEW_SYSTEM,
        tr_flat, glossary, "Claude Opus"
    )

    # Ara kayıt
    tr_path = os.path.join(JSON_DIR, "strings_tr.json")
    save_progress(unflatten_dict(tr_flat), tr_path)
    print(f"  [KAYIT] Opus kontrol sonrası kaydedildi")

    # Geçiş 2: Gemini Pro - son yazım ve tutarlılık kontrolü
    print("\n  [3b] Gemini 2.5 Pro - Son yazım ve tutarlılık kontrolü")
    tr_flat, gemini_fixes = _run_review_pass(
        api_key, GEMINI_PRO_MODEL, GEMINI_PRO_REVIEW_SYSTEM,
        tr_flat, glossary, "Gemini Pro"
    )

    total_fixes = opus_fixes + gemini_fixes
    print(f"\n  [OK] Çift kontrol tamamlandı: {total_fixes} toplam düzeltme")
    print(f"       Claude Opus: {opus_fixes} düzeltme")
    print(f"       Gemini Pro:  {gemini_fixes} düzeltme")
    return tr_flat


# ===================== ANA FONKSİYON =====================

def main():
    print()
    print("=" * 60)
    print("  DON'T STARVE TOGETHER - PRO ÇEVİRİ PIPELINE")
    print("  Gemini Flash (Sozluk) -> Claude Sonnet (Ceviri)")
    print("  -> Kontrol: Claude Opus (devre disi, Opus 4.6 yapacak)")
    print("=" * 60)
    print()

    # Komut satırı argümanları
    import argparse
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--api-key", default="")
    parser.add_argument("--phase", default="")
    args, _ = parser.parse_known_args()

    # API anahtarı
    api_key = args.api_key or os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        print("  OpenRouter API anahtarınızı girin.")
        print("  (https://openrouter.ai/keys adresinden alabilirsiniz)")
        print()
        api_key = input("  API Anahtarı: ").strip()
        if not api_key:
            print("  [HATA] API anahtarı gerekli.")
            sys.exit(1)

    # Bağlantı testi (JSON beklemeyen basit test)
    print("\n  [....] OpenRouter bağlantısı test ediliyor...")
    try:
        resp = requests.post(OPENROUTER_URL, headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }, json={
            "model": GEMINI_MODEL,
            "messages": [{"role": "user", "content": "Say OK"}],
            "max_tokens": 10,
        }, timeout=15)
        if resp.status_code == 200:
            print("  [OK] Bağlantı başarılı!")
        elif resp.status_code == 403:
            print(f"  [HATA] API limiti aşıldı (403). Limit artırın: https://openrouter.ai/settings/keys")
            sys.exit(1)
        elif resp.status_code == 401:
            print(f"  [HATA] Geçersiz API anahtarı (401).")
            sys.exit(1)
        else:
            print(f"  [HATA] API hatası: {resp.status_code} - {resp.text[:200]}")
            sys.exit(1)
    except Exception as e:
        print(f"  [HATA] Bağlantı hatası: {e}")
        sys.exit(1)

    # Kaynak dosyaları kontrol et
    en_path = os.path.join(JSON_DIR, "strings_en.json")
    tr_path = os.path.join(JSON_DIR, "strings_tr.json")

    if not os.path.isfile(en_path):
        print(f"\n  [HATA] İngilizce string dosyası bulunamadı: {en_path}")
        print("  Önce tools/extract/extract_strings.py ile oyun stringlerini çıkarın.")
        sys.exit(1)

    with open(en_path, "r", encoding="utf-8") as f:
        en_data = json.load(f)
    en_flat = flatten_dict(en_data)

    # Mevcut çevirileri yükle
    existing_tr = {}
    if os.path.isfile(tr_path):
        with open(tr_path, "r", encoding="utf-8") as f:
            tr_data = json.load(f)
        existing_tr = flatten_dict(tr_data)

    total = len(en_flat)
    done = sum(1 for v in existing_tr.values() if v.strip())
    remaining = total - done

    print(f"\n  Toplam string:     {total}")
    print(f"  Zaten çevrilmiş:   {done}")
    print(f"  Çevrilecek:        {remaining}")

    if remaining == 0:
        print("\n  Tüm stringler çevrilmiş! Sadece kontrol aşamasını çalıştırıyorum.")
        phase = "3"
    else:
        # Maliyet tahmini
        est_input_tokens = remaining * 60 + total * 20  # çeviri + kontrol
        est_cost = est_input_tokens / 1_000_000 * 5     # kaba tahmin
        print(f"\n  Tahmini maliyet:   ~${est_cost:.2f} (kaba tahmin)")

        if args.phase in ("1", "2", "3"):
            phase = args.phase
            print(f"\n  Asama {phase} secildi (komut satirindan)")
        else:
            print("\n  Hangi asamalardan baslamak istiyorsunuz?")
            print("  [1] Asama 1'den basla (Sozluk -> Ceviri)")
            print("  [2] Asama 2'den basla (Ceviri) - sozluk varsa")
            print("  [3] Sadece Asama 3 (Kontrol) - ceviriler varsa")
            print()
            phase = input("  Seciminiz (1/2/3): ").strip() or "1"

    glossary = {}
    glossary_path = os.path.join(JSON_DIR, "glossary.json")

    # AŞAMA 1
    if phase == "1":
        glossary = phase1_glossary(api_key, en_flat)
    elif os.path.isfile(glossary_path):
        with open(glossary_path, "r", encoding="utf-8") as f:
            glossary = json.load(f)
        print(f"\n  Mevcut sözlük yüklendi: {len(glossary)} terim")

    # AŞAMA 2
    if phase in ("1", "2"):
        tr_flat = phase2_translate(api_key, en_flat, glossary, existing_tr)
        save_progress(unflatten_dict(tr_flat), tr_path)
        print(f"  [KAYIT] Çeviriler kaydedildi: {tr_path}")
    else:
        tr_flat = existing_tr

    # AŞAMA 3 (devre dışı - kontrolü Opus 4.6 yapacak)
    # if phase in ("1", "2", "3"):
    #     tr_flat = phase3_review(api_key, tr_flat, glossary)
    #     save_progress(unflatten_dict(tr_flat), tr_path)
    #     print(f"  [KAYIT] Kontrol sonuçları kaydedildi: {tr_path}")
    if phase == "3":
        print("\n  [BİLGİ] Aşama 3 devre dışı - kontrolü Claude Opus yapacak.")

    # Özet
    final_done = sum(1 for v in tr_flat.values() if v.strip())
    pct = final_done * 100 // max(total, 1)

    print()
    print("=" * 60)
    print("  PRO ÇEVİRİ PIPELINE TAMAMLANDI!")
    print(f"  Çevrilen:  {final_done}/{total} (%{pct})")
    print("=" * 60)
    print()
    print("  Sonraki adımlar:")
    print("  1. data/json/strings_tr.json dosyasını kontrol edin")
    print("  2. python tools/generate/generate_strings_lua.py ile mod dosyasını oluşturun")
    print("  3. Modu oyunda test edin!")
    print()

    # Sözlük istatistikleri
    if glossary:
        print(f"  Sözlük: {len(glossary)} terim (data/json/glossary.json)")
    print(f"  Çeviriler: {tr_path}")


if __name__ == "__main__":
    main()
