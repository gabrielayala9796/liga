import json
import time
from curl_cffi import requests

KEYWORDS = [
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
    "Football"
]

URL = "https://search-ace.stream/search"

HEADERS = {
    "Accept": "application/json",
    "Referer": "https://search-ace.stream/"
}

channels = {}
session = requests.Session()

for keyword in KEYWORDS:
    print(f"Searching: {keyword}")

    try:
        r = session.get(
            URL,
            params={"query": keyword},
            headers=HEADERS,
            impersonate="chrome",
            timeout=15
        )

        if r.status_code != 200:
            print(f"  HTTP {r.status_code}")
            continue

        data = r.json()

        if not isinstance(data, list):
            print("  Unexpected response")
            continue

        for item in data:
            cid = item.get("content_id")
            name = item.get("name")

            if cid and name and cid not in channels:
                channels[cid] = {
                    "name": name,
                    "url": f"acestream://{cid}"
                }

        time.sleep(1)

    except Exception as e:
        print(f"  Error: {e}")

output = list(channels.values())

with open("channels.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Saved {len(output)} channels")
