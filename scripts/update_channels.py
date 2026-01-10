import json
import time
from seleniumbase import SB

CHANNELS = [
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

BASE_URL = "https://search-ace.stream/search?query="


def extract_results(sb, query):
    results = []

    sb.open(BASE_URL + sb.url_encode(query))

    # Esperar Cloudflare + carga real
    sb.wait_for_ready_state_complete()
    time.sleep(5)

    # Cada resultado es un bloque con hash Acestream
    cards = sb.find_elements("div.card")

    for card in cards:
        try:
            title = card.find_element("css selector", ".card-title").text.strip()
            link = card.find_element("css selector", "a").get_attribute("href")

            if "acestream://" in link:
                acestream_hash = link.replace("acestream://", "")
                results.append({
                    "query": query,
                    "title": title,
                    "hash": acestream_hash
                })
        except Exception:
            continue

    return results


def main():
    all_results = []

    with SB(uc=True, headed=True, locale="es") as sb:
        sb.open("https://search-ace.stream")
        sb.sleep(5)  # Cloudflare initial check

        for channel in CHANNELS:
            print(f"Searching: {channel}")
            found = extract_results(sb, channel)
            all_results.extend(found)

    if not all_results:
        print("No channels found")
        return

    with open("channels.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(all_results)} channels")


if __name__ == "__main__":
    main()
