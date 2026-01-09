import json
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
    impersonate="chrome120",  # clave absoluta
)

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Referer": "https://search-ace.stream/",
    "Origin": "https://search-ace.stream",
}

results = []

for term in SEARCH_TERMS:
    print(f"Searching: {term}")

    try:
        r = session.get(
            BASE_URL,
            params={"query": term},
            headers=HEADERS,
            timeout=20,
        )

        print(f"  HTTP {r.status_code}")

        if r.status_code != 200:
            continue

        data = r.json()
        results.extend(data)

        time.sleep(1.2)  # comportamiento humano

    except Exception as e:
        print(f"  Error: {e}")

# eliminar duplicados por content_id
unique = {}
for item in results:
    unique[item["content_id"]] = item

channels = list(unique.values())

with open("channels.json", "w", encoding="utf-8") as f:
    json.dump(channels, f, indent=2, ensure_ascii=False)

print(f"Saved {len(channels)} channels")
