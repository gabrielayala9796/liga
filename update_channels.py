from curl_cffi import requests
import json
import re
from time import sleep

KEYWORDS = [
    "movistar la liga", "liga", "campeones", "dazn", "espn", "futbol",
    "tnt", "ziggo", "nba", "usa", "match", "eleven sport",
    "bein", "setanta", "sky", "sky sports", "bein sports",
    "match football", "tnt sports", "fox sport",
    "movistar liga de campeones", "m liga", "mliga"
]

RESULTS = {}

def extract_hash(text):
    match = re.search(r"\b[a-f0-9]{40}\b", text, re.IGNORECASE)
    return match.group(0) if match else None

for keyword in KEYWORDS:
    print(f"Searching: {keyword}")
    try:
        r = requests.get(
            "https://search-ace.stream/suggestions",
            params={"q": keyword},
            impersonate="chrome120",
            timeout=15
        )

        suggestions = r.json()

        for item in suggestions:
            hash_id = extract_hash(item)
            if hash_id:
                RESULTS[item] = hash_id

        sleep(1)

    except Exception as e:
        print(f"Error fetching '{keyword}': {e}")

channels = [
    {"name": name, "hash": hash_id}
    for name, hash_id in RESULTS.items()
]

with open("channels.json", "w", encoding="utf-8") as f:
    json.dump(channels, f, indent=2, ensure_ascii=False)

print(f"Saved {len(channels)} channels")
