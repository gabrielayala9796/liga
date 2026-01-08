import json
import re
import time
from curl_cffi import requests

KEYWORDS = [
    "movistar liga",
    "liga de campeones",
    "champions",
    "dazn",
    "espn",
    "futbol",
    "tnt",
    "nba",
    "bein",
    "sky sports",
    "fox sport",
    "setanta",
    "eleven sport",
    "match football"
]

SEARCH_URL = "https://search-ace.stream/search"

HEADERS = {
    "accept": "application/json",
    "referer": "https://search-ace.stream/",
}

def is_interesting(name: str) -> bool:
    name = name.lower()
    return any(k in name for k in KEYWORDS)

def extract_hash(text: str):
    m = re.search(r"\b[a-f0-9]{40}\b", text, re.I)
    return m.group(0) if m else None

session = requests.Session(impersonate="chrome")

results = {}

for kw in KEYWORDS:
    print(f"Searching: {kw}")
    try:
        r = session.get(
            SEARCH_URL,
            params={"query": kw},
            headers=HEADERS,
            timeout=15
        )

        data = r.json()

        for item in data:
            name = item.get("name", "")
            content_id = item.get("content_id")

            if not name or not content_id:
                continue

            if is_interesting(name):
                results[name] = content_id

        time.sleep(1)

    except Exception as e:
        print(f"Error with '{kw}': {e}")

channels = [
    {"name": name, "hash": hash_id}
    for name, hash_id in sorted(results.items())
]

with open("channels.json", "w", encoding="utf-8") as f:
    json.dump(channels, f, indent=2, ensure_ascii=False)

print(f"Saved {len(channels)} channels")
