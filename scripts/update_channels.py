import json
import os
import time
from curl_cffi import requests

SEARCH_TERMS = [
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

BASE_URL = "https://search-ace.stream/search"

session = requests.Session(
    impersonate="chrome120",
)

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Referer": "https://search-ace.stream/",
    "Origin": "https://search-ace.stream",
    "Cookie": os.environ.get("CF_COOKIES", ""),
}

results = []

for term in SEARCH_TERMS:
    print(f"Searching: {term}")

    r = session.get(
        BASE_URL,
        params={"query": term},
        headers=headers,
        timeout=20,
    )

    print(f"  HTTP {r.status_code}")

    if r.status_code == 200:
        results.extend(r.json())

    time.sleep(1.5)

unique = {item["content_id"]: item for item in results}

with open("channels.json", "w", encoding="utf-8") as f:
    json.dump(list(unique.values()), f, indent=2, ensure_ascii=False)

print(f"Saved {len(unique)} channels")
