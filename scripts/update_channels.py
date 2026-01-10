from playwright.sync_api import sync_playwright
import json
import time
from urllib.parse import quote_plus

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
    "Football"
]

results = []

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")

    # Usa el primer contexto existente o crea uno
    context = browser.contexts[0] if browser.contexts else browser.new_context()

    # CREA una pestaña nueva (clave)
    page = context.new_page()

    for channel in CHANNELS:
        print(f"Searching: {channel}")
        url = f"https://search-ace.stream/search?query={quote_plus(channel)}"
        page.goto(url, timeout=60000)
        page.wait_for_load_state("networkidle")
        time.sleep(2)

        links = page.locator("a[href^='acestream://']").all()

        if not links:
            print("  No results")
            continue

        for link in links:
            ace = link.get_attribute("href")
            results.append({
                "name": channel,
                "acestream": ace
            })

        print(f"  Found {len(links)}")

with open("channels.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("channels.json updated")
