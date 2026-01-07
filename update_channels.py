import requests
import json
import time

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

def fetch(keyword: str):
    try:
        r = requests.get(API_URL, params={"q": keyword}, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[ERROR] {keyword}: {e}")
        return []

def main():
    seen = set()
    channels = []

    for kw in KEYWORDS:
        print(f"[INFO] buscando: {kw}")
        results = fetch(kw)

        for item in results:
            cid = item.get("content_id")
            name = item.get("name")

            if not cid or not name:
                continue

            if cid in seen:
                continue

            seen.add(cid)
            channels.append({
                "name": name.strip(),
                "hash": cid
            })

        time.sleep(1)

    channels.sort(key=lambda x: x["name"].lower())

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(channels, f, indent=2, ensure_ascii=False)

    print(f"[OK] {len(channels)} canales guardados")

if __name__ == "__main__":
    main()
