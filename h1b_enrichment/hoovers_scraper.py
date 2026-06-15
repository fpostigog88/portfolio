"""Hoovers CDP - Working company search and data enrichment via Chrome Redux.
================================================================
Uses Chrome's logged-in session + React/Redux to search companies and extract:
  - Company name, employees, revenue (USD), city, state, country

This is the CORE DISCOVERY:
  1. Type in search input using React synthetic events
  2. Redux globalSearch.searchResults[] holds rich company data
  3. Data includes: companyName, numEmployees, salesUsd, addresses[], id

Usage:
    python hoovers_scraper.py search "Apple Inc"
    python hoovers_scraper.py batch companies.txt
    python hoovers_scraper.py test
"""

import subprocess
import json
import time
import sys
import os

CDP_HOST = "localhost"
CDP_PORT = 9522
TARGET_ID = "D72FC6FE586092C1931250FB7935B285"
WS_URL = f"ws://{CDP_HOST}:{CDP_PORT}/devtools/page/{TARGET_ID}"


def cdp(js, timeout=25):
    script = f"""
const WebSocket = require('ws');
const ws = new WebSocket('{WS_URL}');
ws.on('open', () => {{
    ws.send(JSON.stringify({{ id: 1, method: 'Runtime.evaluate', params: {{ expression: `{js.replace('`', '` + "`" + `')}`, returnByValue: true }} }}));
    ws.on('message', (data) => {{
        const msg = JSON.parse(data);
        if (msg.id === 1) {{ console.log(JSON.stringify(msg.result || msg)); ws.close(); }}
    }});
}});
ws.on('error', (e) => {{ console.log(JSON.stringify({{error: e.message}})); ws.close(); }});
"""
    r = subprocess.run(["node", "-e", script], capture_output=True, text=True, timeout=timeout)
    try:
        return json.loads(r.stdout.strip())
    except:
        return {"raw": r.stdout or r.stderr}


def navigate(url):
    cdp(f"window.location.href='{url}'")
    time.sleep(2)


def search_company(name, max_results=5):
    """
    Search for a company in Hoovers and return results from Redux.
    Returns list of dicts with: companyName, numEmployees, salesUsd, city, state, country
    """
    # Navigate to search page
    navigate("https://app.hoovers.dnb.com/search/company")
    time.sleep(2)

    # Type using React synthetic event
    name_esc = name.replace("'", "\\'")
    r = cdp(f"""
(function() {{
    var input = document.querySelector('input.ant-input-lg');
    if (!input) return 'not found';
    var nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
    nativeSetter.call(input, '{name_esc}');
    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
    return 'typed: ' + input.value;
}})()
""")
    time.sleep(2)

    # Extract results from Redux
    r = cdp(f"""
(function() {{
    var state = window.store.getState();
    var gs = state.globalSearch;
    var results = gs.searchResults || [];
    return JSON.stringify({{
        count: results.length,
        companies: results.map(function(r) {{
            return {{
                companyName: r.companyName || '',
                numEmployees: r.numEmployees || 0,
                salesUsd: r.salesUsd || 0,
                city: r.addresses && r.addresses[0] ? (r.addresses[0].city || '') : '',
                stateName: r.addresses && r.addresses[0] && r.addresses[0].stateOrProvince ? (r.addresses[0].stateOrProvince.name || '') : '',
                countryName: r.addresses && r.addresses[0] && r.addresses[0].country ? (r.addresses[0].country.name || '') : '',
                id: r.id || ''
            }};
        }}).slice(0, {max_results})
    }});
}})()
""")
    time.sleep(1)

    try:
        data = r.get("result", {}).get("value", r.get("value", "{}"))
        if isinstance(data, str):
            data = json.loads(data)
        return data
    except:
        return {"count": 0, "companies": []}


def format_currency(amount):
    """Format USD amount as $X Billion/Million."""
    if not amount:
        return ""
    try:
        amount = float(amount)
        if amount >= 1_000_000_000:
            return f"${amount/1_000_000_000:.2f}B"
        elif amount >= 1_000_000:
            return f"${amount/1_000_000:.2f}M"
        else:
            return f"${amount:,.0f}"
    except:
        return str(amount)


def enrich_company(name, max_results=3):
    """
    Search for a company and return the best match enriched data.
    Returns: source_name, matched_name, employees, revenue, city, state, country, hoovers_id
    """
    results = search_company(name, max_results=max_results)
    companies = results.get("companies", [])

    if not companies:
        return {"source_name": name, "error": "not found"}

    # Return first/best match
    best = companies[0]
    return {
        "source_name": name,
        "matched_name": best.get("companyName", ""),
        "employees": best.get("numEmployees", 0),
        "revenue": format_currency(best.get("salesUsd", 0)),
        "revenue_raw": best.get("salesUsd", 0),
        "city": best.get("city", ""),
        "state": best.get("stateName", ""),
        "country": best.get("countryName", ""),
        "hoovers_id": best.get("id", ""),
    }


def batch_enrich(filepath, limit=100, delay=1.5, save_every=25):
    """Enrich companies from a text file (one name per line). Saves incrementally."""
    with open(filepath, encoding='utf-8') as f:
        companies = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    companies = companies[:limit]
    results = []
    output_path = filepath.replace(".txt", "_enriched.csv")

    # Load existing results if any (resume support)
    if os.path.exists(output_path):
        try:
            import csv as csvmod
            with open(output_path, 'r', encoding='utf-8') as f:
                reader = csvmod.DictReader(f)
                existing = {row['source_name']: row for row in reader}
            results = list(existing.values())
            already_done = set(existing.keys())
            print(f"Resuming: {len(results)} already done, {len(companies) - len(results)} remaining", flush=True)
            companies = [c for c in companies if c not in already_done]
        except Exception as e:
            print(f"Could not load existing CSV: {e}", flush=True)
            already_done = set()
    else:
        already_done = set()

    for i, company in enumerate(companies):
        print(f"[{len(results)+1}/{limit}] {company}", flush=True)
        data = enrich_company(company)
        results.append(data)

        if data.get("error"):
            print(f"  -> NOT FOUND")
        else:
            print(f"  -> {data.get('matched_name', 'N/A')} | {data.get('employees', 'N/A')} employees | {data.get('revenue', 'N/A')} | {data.get('city', 'N/A')}, {data.get('state', 'N/A')}")

        # Save every N records
        if len(results) % save_every == 0:
            save_csv(results, output_path)
            print(f"  [CHECKPOINT: {len(results)} saved]", flush=True)

        time.sleep(delay)

    # Final save
    save_csv(results, output_path)
    return results


def save_csv(results, output_path):
    """Save enrichment results to CSV."""
    if not results:
        return

    import csv
    fieldnames = list(results[0].keys())
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(results)

    print(f"\nSaved {len(results)} records to: {output_path}")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    args = sys.argv[2:]

    if cmd == "search":
        name = " ".join(args)
        print(f"Searching: {name}")
        data = enrich_company(name)
        print(json.dumps(data, indent=2))

    elif cmd == "batch":
        filepath = args[0] if args else "companies.txt"
        limit = int(args[1]) if len(args) > 1 else 100
        print(f"Batch enrichment from: {filepath} (limit: {limit})")
        results = batch_enrich(filepath, limit=limit)
        output = filepath.replace(".txt", "_enriched.csv")
        # Already saved by batch_enrich
        print(f"\nTotal: {len(results)} records saved to: {output}")

    elif cmd == "test":
        # Test search
        print("Testing search for Apple...")
        results = search_company("Apple", max_results=3)
        print(f"Found {results.get('count', 0)} results:")
        for c in results.get("companies", []):
            print(f"  {c.get('companyName')} | {c.get('numEmployees')} employees | {format_currency(c.get('salesUsd'))} | {c.get('city')}, {c.get('stateName')}")

    elif cmd == "h1b":
        # Enrich H-1B California employers
        h1b_path = args[0] if args else "california_h1b_enriched.csv"
        if not os.path.exists(h1b_path):
            print(f"H-1B file not found: {h1b_path}")
            print("Run: python run_enrichment.py --california")
            sys.exit(1)

        import csv
        with open(h1b_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            companies = [row.get("Employer", row.get("employer", "")) for row in reader]
            companies = [c for c in companies if c]

        print(f"Enriching {len(companies)} H-1B employers...")
        results = batch_enrich(h1b_path, limit=len(companies))

        output = h1b_path.replace(".csv", "_hoovers_enriched.csv")
        save_csv(results, output)

    else:
        print("Usage:")
        print("  python hoovers_scraper.py test                    # Test with Apple")
        print("  python hoovers_scraper.py search \"Company Name\"   # Single search")
        print("  python hoovers_scraper.py batch companies.txt     # Batch from file")
        print("  python hoovers_scraper.py h1b [california_h1b_enriched.csv]")


if __name__ == "__main__":
    main()
