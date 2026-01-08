import json
import re
import time
from curl_cffi import requests

KEYWORDS = [
    "movistar la liga", "liga", "campeones", "dazn", "espn", "futbol",
    "tnt", "ziggo", "nba", "usa", "match", "eleven sport",
    "bein", "setanta", "sky", "sky sports", "bein sports",
    "match football", "tnt sports", "fox sport",
    "movistar liga de campeones", "m liga", "mliga"
]

URL = "https://search-ace.stream/suggestions"

HEADERS = {
    "Accept": "*/*",
    "Referer": "https://search-ace.stream/",
}

HASH_REGEX = re.compile(r"\b[a-f0-9]{40}\b", re.IGNORECASE)

results = {}

def extract_hash(text: str):
    match = HASH_REGEX.search(text)
    return match.group(0) if match else None


for keyword in KEYWORDS:
    print(f"Searching: {keyword}")

    try:
        r = requests.get(
            URL,
            params={"q": keyword},
            headers=HEADERS,
            impersonate="chrome",   # CLAVE
            timeout=15
        )

        if r.status_code != 200:
            print(f"  HTTP {r.status_code}")
            continue

        data = r.json()

        for item in data:
            h = extract_hash(item)
            if h and item not in results:
                results[item] = h

        time.sleep(1)  # evita rate-limit

    except Exception as e:
        print(f"  Error: {e}")


channels = [
    {
        "name": name,
        "url": f"acestream://{hash_id}"
    }
    for name, hash_id in results.items()
]

with open("channels.json", "w", encoding="utf-8") as f:
    json.dump(channels, f, indent=2, ensure_ascii=False)

print(f"Saved {len(channels)} channels")
