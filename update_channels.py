import json
import requests
import re
from pathlib import Path

# ----------------------------
# CONFIGURACIÓN
# ----------------------------

API_URL = "https://search-ace.stream/search"

RAW_KEYWORDS = [
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
    "m liga",
    "mliga"
]

OUTPUT_FILE = Path("channels.json")

# ----------------------------
# UTILIDADES
# ----------------------------

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9 ]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

KEYWORDS = [normalize(k) for k in RAW_KEYWORDS]

# ----------------------------
# LÓGICA PRINCIPAL
# ----------------------------

def fetch_channels(query: str):
    response = requests.get(API_URL, params={"q": query}, timeout=15)
    response.raise_for_status()
    return response.json()

def main():
    collected = {}
    
    for keyword in RAW_KEYWORDS:
        print(f"Searching: {keyword}")
        try:
            results = fetch_channels(keyword)
        except Exception as e:
            print(f"Error fetching '{keyword}': {e}")
            continue

        for channel in results:
            name = channel.get("name", "")
            cid = channel.get("content_id")

            if not name or not cid:
                continue

            normalized_name = normalize(name)

            if any(k in normalized_name for k in KEYWORDS):
                collected[cid] = {
                    "name": name,
                    "content_id": cid,
                    "pid": channel.get("pid")
                }
                print(f"  MATCH: {name}")

    final_list = sorted(collected.values(), key=lambda x: x["name"].lower())

    OUTPUT_FILE.write_text(
        json.dumps(final_list, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"\nSaved {len(final_list)} channels to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
