import json
import time
import urllib.parse
from pathlib import Path
from curl_cffi import requests

# =========================
# CONFIG
# =========================

BASE_URL = "https://search-ace.stream/search?query="
OUTPUT_FILE = Path("channels.json")

CHANNEL_QUERIES = [
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
    "Referer": "https://search-ace.stream/",
}

# =========================
# LOGIC
# =========================

def fetch_channels(query: str):
    encoded = urllib.parse.quote_plus(query)
    url = BASE_URL + encoded

    print(f"Searching: {query}")

    resp = requests.get(
        url,
        headers=HEADERS,
        impersonate="chrome"
    )

    if resp.status_code != 200:
        print(f"  HTTP {resp.status_code}")
        return []

    try:
        data = resp.json()
    except Exception:
        print("  Invalid JSON response")
        return []

    results = []

    for item in data:
        acestream_id = item.get("infohash") or item.get("hash")
        name = item.get("name") or query

        if not acestream_id:
            continue

        results.append({
            "name": name.strip(),
            "acestream": f"acestream://{acestream_id}"
        })

    print(f"  Results found: {len(results)}")
    return results


def main():
    all_channels = []

    for query in CHANNEL_QUERIES:
        all_channels.extend(fetch_channels(query))
        time.sleep(1)  # pequeña pausa para no levantar sospechas

    if not all_channels:
        print("No channels found")
        return

    OUTPUT_FILE.write_text(
        json.dumps(all_channels, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print("channels.json updated successfully")


if __name__ == "__main__":
    main()
