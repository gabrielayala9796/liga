import os
import json
import time
import subprocess
from pathlib import Path
from urllib.parse import quote_plus
from seleniumbase import SB

# ============================================================
#  DETECTAR RAÍZ REAL DEL PROYECTO (LOCAL + GITHUB ACTIONS)
# ============================================================

def get_project_root():
    # 1) GitHub Actions
    github_workspace = os.environ.get("GITHUB_WORKSPACE")
    if github_workspace:
        return Path(github_workspace).resolve()

    # 2) Local usando git
    try:
        result = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()
        return Path(result).resolve()
    except Exception:
        pass

    # 3) Fallback absoluto (último recurso)
    return Path(__file__).resolve().parents[1]


PROJECT_ROOT = get_project_root()
OUTPUT_FILE = PROJECT_ROOT / "channels.json"

print(f"[INFO] Project root detected as: {PROJECT_ROOT}")
print(f"[INFO] channels.json will be written to: {OUTPUT_FILE}")

# ============================================================
#  CONFIGURACIÓN
# ============================================================

BASE_URL = "https://search-ace.stream"
SEARCH_URL = "https://search-ace.stream/search?query={}"

CHANNEL_QUERIES = [
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

# ============================================================
#  ESPERA ROBUSTA (CLOUDFLARE)
# ============================================================

def wait_for_site_ready(sb, timeout=60):
    print("Waiting for full page load...")
    sb.wait_for_ready_state_complete(timeout=timeout)

    # Cloudflare suele finalizar DESPUÉS del readyState
    print("Waiting extra time for Cloudflare challenge to fully settle...")
    time.sleep(10)

    # Verificación mínima de ejecución JS
    sb.execute_script("return document.body")
    print("Site ready. JS execution confirmed.")

# ============================================================
#  FETCH SEARCH RESULTS (JSON DIRECTO)
# ============================================================

def fetch_search_results(sb, query):
    encoded_query = quote_plus(query)
    url = SEARCH_URL.format(encoded_query)

    script = """
    const callback = arguments[arguments.length - 1];
    fetch(arguments[0])
        .then(resp => resp.json())
        .then(data => callback(data))
        .catch(err => callback([]));
    """

    return sb.execute_async_script(script, url)

# ============================================================
#  MAIN
# ============================================================

def main():
    all_results = []

    with SB(
        uc=True,
        headless=True,
        disable_js=False,
        window_size="1920,1080"
    ) as sb:

        print("Opening base URL...")
        sb.open(BASE_URL)

        wait_for_site_ready(sb)

        for query in CHANNEL_QUERIES:
            print(f"Searching: {query}")
            results = fetch_search_results(sb, query)

            if not results:
                print("  No results")
                continue

            print(f"  Found: {len(results)}")

            for item in results:
                if not isinstance(item, dict):
                    continue

                all_results.append({
                    "query": query,
                    "name": item.get("name"),
                    "translated_name": item.get("translated_name"),
                    "content_id": item.get("content_id"),
                    "pid": item.get("pid"),
                })

    # ========================================================
    #  GUARDAR SIEMPRE EN LA RAÍZ DEL PROYECTO
    # ========================================================

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(all_results)} channels to {OUTPUT_FILE}")

# ============================================================

if __name__ == "__main__":
    main()
