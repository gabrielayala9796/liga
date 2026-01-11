import json
from pathlib import Path
# Ruta absoluta a la raíz del proyecto (Liga)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FILE = PROJECT_ROOT / "channels.json"

import json
import time
from seleniumbase import SB
from urllib.parse import quote_plus

BASE_URL = "https://search-ace.stream"
SEARCH_URL = BASE_URL + "/search?query="

CHANNELS = [
    "M+ Liga de Campeones FHD",
    "Movistar La Liga",
    "La Liga",
    "Champions",
    "DAZN",
    "ESPN",
    "TNT Sports",
    "TNT",
    "Bein Sports",
    "Sky Sports",
    "NBA",
    "Football",
]

OUTPUT_FILE = "channels.json"


def wait_for_site_ready(sb):
    print("Opening base URL (headless)...")
    sb.open(BASE_URL)

    print("Waiting for full page load...")
    sb.wait_for_ready_state_complete(timeout=60)

    print("Waiting extra time for Cloudflare challenge to fully settle...")
    time.sleep(25)

    # Confirm JS execution works
    test_script = """
        const cb = arguments[arguments.length - 1];
        fetch('/search?query=test')
            .then(r => r.json())
            .then(() => cb(true))
            .catch(() => cb(false));
    """
    ok = sb.execute_async_script(test_script, timeout=30)
    if not ok:
        raise RuntimeError("Site not ready for JS execution")

    print("Site ready. JS execution confirmed.")


def fetch_search_results(sb, query):
    url = SEARCH_URL + quote_plus(query)

    script = f"""
        const cb = arguments[arguments.length - 1];
        fetch("{url}")
            .then(r => r.json())
            .then(data => cb(data))
            .catch(err => cb({{error: err.toString()}}));
    """
    return sb.execute_async_script(script, timeout=30)


def main():
    collected = []

    with SB(
        uc=True,
        headless=True,
        incognito=True,
        window_size="1920,1080"
    ) as sb:

        wait_for_site_ready(sb)

        for channel in CHANNELS:
            print(f"Searching: {channel}")
            time.sleep(2)

            results = fetch_search_results(sb, channel)

            if isinstance(results, dict) and "error" in results:
                print("  Fetch error:", results["error"])
                continue

            if not isinstance(results, list):
                print("  Unexpected response format")
                continue

            found = 0
            for item in results:
                if not isinstance(item, dict):
                    continue

                content_id = item.get("content_id")
                if not content_id:
                    continue

                collected.append({
                    "query": channel,
                    "name": item.get("name"),
                    "translated_name": item.get("translated_name"),
                    "content_id": content_id,
                    "pid": item.get("pid"),
                })
                found += 1

            print(f"  Found: {found}")

        if not collected:
            print("No channels found")
            return

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(collected, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(collected)} channels to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
