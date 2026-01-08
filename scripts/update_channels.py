import json
import time
from curl_cffi import requests

SEARCH_URL = "https://search-ace.stream/search"

QUERIES = [
    "M+ Liga de Campeones FHD",
    "Movistar La Liga",
    "La Liga",
    "Liga",
    "Champions",
    "DAZN",
    "ESPN",
    "TNT Sports",
    "Bein Sports",
    "Sky Sports",
    "NBA",
    "Football",
]

HEADERS = {
    "accept": "application/json",
    "accept-language": "es,en-US;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
}

session = requests.Session(
    impersonate="chrome",
    headers=HEADERS,
)

channels = []

for query in QUERIES:
    print(f"Searching: {query}")
    try:
        response = session.get(
            SEARCH_URL,
            params={"query": query},
            timeout=30,
        )

        if response.status_code != 200:
            print(f"  HTTP {response.status_code}")
            continue

        data = response.json()
        if isinstance(data, list):
            channels.extend(data)
            print(f"  Found {len(data)} results")

        time.sleep(1)

    except Exception as e:
        print(f"  Error: {e}")

# Eliminar duplicados por content_id
unique = {}
for ch in channels:
    cid = ch.get("content_id")
    if cid:
        unique[cid] = ch

channels = list(unique.values())

with open("channels.json", "w", encoding="utf-8") as f:
    json.dump(channels, f, indent=2, ensure_ascii=False)

print(f"Saved {len(channels)} channels")
