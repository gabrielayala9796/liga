import json
import re
from pathlib import Path
from curl_cffi import requests

# =========================
# CONFIGURACIÓN
# =========================

BASE_URL = "https://search-ace.stream/search"
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
    "Football",
]

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "referer": "https://search-ace.stream/",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/143.0.0.0 Safari/537.36"
    ),
    "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-ch-ua-arch": '"x86"',
    "sec-ch-ua-bitness": '"64"',
}

ACE_HASH_REGEX = re.compile(r"(?:acestream://)?([a-fA-F0-9]{40})")

# =========================
# FUNCIONES
# =========================

def search_channel(query: str) -> list[dict]:
    print(f"Searching: {query}")

    r = requests.get(
        BASE_URL,
        params={"query": query},
        headers=HEADERS,
        impersonate="chrome",
        timeout=30,
    )

    if r.status_code != 200:
        print(f"  HTTP {r.status_code}")
        return []

    try:
        data = r.json()
    except Exception as e:
        print(f"  JSON error: {e}")
        return []

    return data.get("results", [])


def extract_acestream(entry: dict) -> str | None:
    for value in entry.values():
        if not isinstance(value, str):
            continue
        match = ACE_HASH_REGEX.search(value)
        if match:
            return match.group(1)
    return None


# =========================
# MAIN
# =========================

def main():
    channels = []

    for query in CHANNEL_QUERIES:
        results = search_channel(query)

        if not results:
            continue

        for item in results:
            name = item.get("name") or item.get("title") or query
            ace_hash = extract_acestream(item)

            if not ace_hash:
                continue

            channels.append({
                "name": name.strip(),
                "acestream": ace_hash.lower(),
            })

    if not channels:
        print("No channels found")
        return

    # Eliminar duplicados por hash
    unique = {c["acestream"]: c for c in channels}
    final_channels = list(unique.values())

    OUTPUT_FILE.write_text(
        json.dumps(final_channels, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"channels.json updated successfully ({len(final_channels)} channels)")


if __name__ == "__main__":
    main()
