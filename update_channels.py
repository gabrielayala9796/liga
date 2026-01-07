import requests
import json
import time

# ========= CONFIGURACIÓN =========

API_URL = "https://search-ace.stream/search"
KEYWORDS = [
    "movistar la liga",
    "liga",
    "campeones",
    "dazn",
    "espn",
    "futbol",
    "tnt",
    "ziggo",
    "nba",
    "usa",
    "match",
    "eleven sport",
    "bein",
    "setanta",
    "sky",
    "sky sports",
    "bein sports",
    "match football",
    "tnt sports",
    "fox sport",
    "movistar liga de campeones",
    "m. liga",
    "m.liga"
]

OUTPUT_FILE = "channels.json"

# ========= LÓGICA =========

def normalize(text: str) -> str:
    return text.lower()

def fetch_channels(keyword: str):
    try:
        response = requests.get(API_URL, params={"q": keyword}, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[ERROR] {keyword}: {e}")
        return []

def main():
    seen_hashes = set()
    channels = []

    for keyword in KEYWORDS:
        print(f"[INFO] Buscando: {keyword}")
        results = fetch_channels(keyword)

        for item in results:
            content_id = item.get("content_id")
            name = item.get("name", "").strip()

            if not content_id or not name:
                continue

            if content_id in seen_hashes:
                continue

            # Filtro básico de relevancia
            name_norm = normalize(name)
            if not any(k in name_norm for k in ["liga", "sport", "futbol", "nba", "football"]):
                continue

            seen_hashes.add(content_id)
            channels.append({
                "name": name,
                "hash": content_id
            })

        time.sleep(1)  # evita rate-limit

    # Ordenar alfabéticamente
    channels.sort(key=lambda x: x["name"].lower())

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(channels, f, indent=2, ensure_ascii=False)

    print(f"[OK] Generado {OUTPUT_FILE} con {len(channels)} canales")

if __name__ == "__main__":
    main()
