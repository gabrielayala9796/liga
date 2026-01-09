import json
import time
from curl_cffi import requests

BASE_URL = "https://search-ace.stream/search"

QUERIES = [
    "M+ Liga de Campeones FHD",
    "Movistar La Liga",
    "La Liga",
    "Champions",
    "DAZN",
    "ESPN",
    "TNT Sports",
    "Bein Sports",
    "Sky Sports",
    "NBA",
    "Football"
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://search-ace.stream/",
}

session = requests.Session(impersonate="chrome")

channels = {}

for query in QUERIES:
    print(f"Searching: {query}")

    try:
        r = session.get(
            BASE_URL,
            params={"query": query},
            headers=HEADERS,
            timeout=20
        )

        if r.status_code != 200:
            print(f"  HTTP {r.status_code}")
            continue

        data = r.json()

        if not isinstance(data, list):
            print("  Unexpected response format")
            continue

        for item in data:
            name = item.get("name")
            content_id = item.get("content_id")

            if name and content_id:
                channels[name] = content_id

        time.sleep(1)

    except Exception as e:
        print(f"  Error: {e}")

with open("channels.json", "w", encoding="utf-8") as f:
    json.dump(channels, f, indent=2, ensure_ascii=False)

print(f"Saved {len(channels)} channels")
