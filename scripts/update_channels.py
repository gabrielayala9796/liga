from playwright.sync_api import sync_playwright
import json
import time

SEARCH_URL = "https://search-ace.stream"

QUERY = "M+ Liga de Campeones FHD"

with sync_playwright() as p:
    print("Connecting to real Chrome via CDP...")

    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")

    context = browser.contexts[0]
    page = context.pages[0] if context.pages else context.new_page()

    print("Navigating...")
    page.goto(SEARCH_URL, wait_until="networkidle")
    time.sleep(5)

    # Espera explícita y segura
    page.wait_for_selector("input", timeout=60000)

    print(f"Searching: {QUERY}")
    page.fill("input", QUERY)
    page.keyboard.press("Enter")

    time.sleep(8)

    # Captura resultados (ejemplo)
    results = page.locator("a").all_inner_texts()

    print("Results found:", len(results))

    with open("channels.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("channels.json updated successfully")
