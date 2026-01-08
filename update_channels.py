from curl_cffi import requests
import json
import time

SEARCH_TERMS = [
    "movistar la liga",
    "liga",
    "campeones",
    "dazn",
    "espn",
    "futbol",
    "tnt",
    "ziggo",
    "nba",
    "usa",
    "match",
    "eleven sport",
    "bein",
    "setanta",
    "sky",
    "sky sports",
    "bein sports",
    "match football",
    "tnt sports",
    "fox sport",
    "movistar liga de campeones",
    "m liga",
    "mliga",
]

BASE_URL = "https://search-ace.stream/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}

def fetch(term: str):
    try:
        resp = requests.get(
            BASE_URL,
            params={"q": term},
            headers=HEADERS,
            timeout=20,
        )

        print("=" * 80)
        print(f"SEARCH TERM: {term}")
        print("STATUS CODE:", resp.status_code)
        print("CONTENT-TYPE:", resp.headers.get("content-type"))
        print("RESPONSE (first 500 chars):")
        print(resp.text[:500])
        print("=" * 80)

        time.sleep(1)

    except Exception as e:
        print(f"Request failed for '{term}': {e}")

def main():
    for term in SEARCH_TERMS:
        fetch(term)

    # No escribimos channels.json todavía
    print("Diagnostic run completed")

if __name__ == "__main__":
    main()
