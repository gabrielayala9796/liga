from playwright.sync_api import sync_playwright
import json
import re
import time

KEYWORDS = [
    "M+ Liga de Campeones FHD",
    "Movistar La Liga",
    "La Liga",
    "Champions",
    "DAZN",
    "ESPN"
]

def extract_hash(text):
    match = re.search(r"\b[a-f0-9]{40}\b", text, re.I)
    return match.group(0) if match else None

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://search-ace.stream", timeout=60000)
    page.wait_for_timeout(8000)  # Cloudflare

    for keyword in KEYWORDS:
        print(f"Searching: {keyword}")

        page.fill("input[type='search']", "")
        page.fill("input[type='search']", keyword)
        page.keyboard.press("Enter")

        page.wait_for_timeout(3000)

        items = page.locator(".list-group-item").all_text_contents()

        for item in items:
            h = extract_hash(item)
            if h:
                results[item] = h

    browser.close()

channels = [{"name": k, "hash": v} for k, v in results.items()]

with open("channels.json", "w", encoding="utf-8") as f:
    json.dump(channels, f, indent=2, ensure_ascii=False)

print(f"Saved {len(channels)} channels")
