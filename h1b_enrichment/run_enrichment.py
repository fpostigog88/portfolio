"""
H-1B Employer Data Enrichment Pipeline
=====================================
Works in two modes:

MODE 1 - AGENT CDP MODE (recommended):
  The agent uses browser_cdp tool directly to scrape Hoovers.
  The Python script processes CSV data only.

MODE 2 - STANDALONE (requires Hoovers CSV download):
  python run_enrichment.py --all-us
  Produces filtered/deduplicated company lists for manual enrichment.

Workflow:
  1. Download H-1B CSV from Tableau (manual)
  2. python run_enrichment.py --california  (filter CA employers)
  3. Agent uses CDP to enrich via Hoovers
  4. python merge_results.py  (combine and export)

Quick Start:
  1. Download CSV from: https://bigdataanalyticspub-sb.uscis.dhs.gov/views/H1BEmployerDataHub-Final/H1B-EmployerDataHub
  2. python run_enrichment.py --california
  3. Tell the agent: "Use CDP to enrich the california_h1b_enriched.csv companies in h1b_enrichment/"
"""

import os
import sys
import csv
import json
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).parent
H1B_CSV_PATH = BASE_DIR / "H1B_Employer_Data.csv"
CALIFORNIA_OUTPUT = BASE_DIR / "california_h1b_enriched.csv"
ALL_US_OUTPUT = BASE_DIR / "all_us_h1b_enriched.csv"
ENRICHED_OUTPUT = BASE_DIR / "california_h1b_final.csv"

# State FIPS codes
STATE_CODES = {
    "AL": "01", "AK": "02", "AZ": "04", "AR": "05", "CA": "06",
    "CO": "08", "CT": "09", "DE": "10", "FL": "12", "GA": "13",
    "HI": "15", "ID": "16", "IL": "17", "IN": "18", "IA": "19",
    "KS": "20", "KY": "21", "LA": "22", "ME": "23", "MD": "24",
    "MA": "25", "MI": "26", "MN": "27", "MS": "28", "MO": "29",
    "MT": "30", "NE": "31", "NV": "32", "NH": "33", "NJ": "34",
    "NM": "35", "NY": "36", "NC": "37", "ND": "38", "OH": "39",
    "OK": "40", "OR": "41", "PA": "42", "RI": "44", "SC": "45",
    "SD": "46", "TN": "47", "TX": "48", "UT": "49", "VT": "50",
    "VA": "51", "WA": "53", "WV": "54", "WI": "55", "WY": "56",
    "DC": "11"
}

STATE_NAMES = {
    "CA": "California", "NY": "New York", "TX": "Texas", "FL": "Florida",
    "IL": "Illinois", "PA": "Pennsylvania", "OH": "Ohio", "GA": "Georgia",
    "NC": "North Carolina", "MI": "Michigan", "NJ": "New Jersey", "VA": "Virginia",
    "WA": "Washington", "AZ": "Arizona", "MA": "Massachusetts", "CO": "Colorado",
    "TN": "Tennessee", "MN": "Minnesota", "IN": "Indiana", "MO": "Missouri",
    "MD": "Maryland", "WI": "Wisconsin", "CT": "Connecticut", "OR": "Oregon",
    "OK": "Oklahoma", "NV": "Nevada", "KY": "Kentucky", "LA": "Louisiana",
    "IA": "Iowa", "UT": "Utah", "AR": "Arkansas", "KS": "Kansas",
    "MS": "Mississippi", "NE": "Nebraska", "NM": "New Mexico", "ID": "Idaho",
    "HI": "Hawaii", "NH": "New Hampshire", "ME": "Maine", "MT": "Montana",
    "RI": "Rhode Island", "DE": "Delaware", "SD": "South Dakota", "AK": "Alaska",
    "ND": "North Dakota", "VT": "Vermont", "WY": "Wyoming", "DC": "District of Columbia",
    "WV": "West Virginia"
}


def load_h1b_csv(path):
    """Load H-1B employer data from CSV."""
    if not os.path.exists(path):
        return None

    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    return rows


def detect_columns(rows):
    """Auto-detect column names for employer name and state."""
    if not rows:
        return 'Employer', 'State'

    sample = rows[0]
    name_col = None
    state_col = None

    for key in sample.keys():
        k_lower = key.lower()
        if not name_col and any(x in k_lower for x in ['employer', 'petitioner', 'legal name', 'name']):
            if 'city' not in k_lower and 'address' not in k_lower:
                name_col = key
        if not state_col and any(x in k_lower for x in ['state', 'province', 'subdivision']):
            state_col = key

    return name_col or 'Employer', state_col or 'State'


def filter_by_state(rows, state_code, name_col, state_col):
    """Filter rows by state code."""
    code_upper = state_code.upper()
    code_name = STATE_NAMES.get(code_upper, "").upper()

    filtered = []
    for row in rows:
        state_val = str(row.get(state_col, row.get('State', ''))).strip().upper()
        if (state_val == code_upper or
            state_val == code_name or
            state_val == STATE_CODES.get(code_upper, '') or
            code_upper in state_val):
            filtered.append(row)

    return filtered


def deduplicate(rows, name_col):
    """Deduplicate by employer name."""
    seen = {}
    for row in rows:
        name = str(row.get(name_col, '')).strip()
        if not name:
            continue
        name_lower = name.lower()
        seen[name_lower] = row
    return list(seen.values())


def export_companies(rows, name_col, output_path):
    """Export company names to CSV."""
    if not rows:
        print(f"No data to export")
        return 0

    fieldnames = list(rows[0].keys()) if rows else [name_col]
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


def get_top_employers(rows, name_col, n=50):
    """Get top N employers by row count (proxy for H-1B volume)."""
    counts = {}
    for row in rows:
        name = str(row.get(name_col, '')).strip()
        if name:
            counts[name] = counts.get(name, 0) + 1

    sorted_employers = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_employers[:n]


def main():
    parser = argparse.ArgumentParser(description="H-1B Employer Data Processor")
    parser.add_argument('--california', action='store_true', help='Filter California only')
    parser.add_argument('--all-us', action='store_true', help='Process all US states')
    parser.add_argument('--top', type=int, default=0, help='Export top N employers only')
    parser.add_argument('--input', default=str(H1B_CSV_PATH), help='Input H1B CSV path')
    parser.add_argument('--output', default=None, help='Output CSV path')
    args = parser.parse_args()

    print("=" * 60)
    print("H-1B Employer Data Processor")
    print("=" * 60)

    # Load data
    print(f"\nLoading: {args.input}")
    rows = load_h1b_csv(args.input)

    if rows is None:
        print(f"\nERROR: H1B CSV not found at {args.input}")
        print("\nTo get the H-1B data:")
        print("  1. Go to: https://bigdataanalyticspub-sb.uscis.dhs.gov/views/H1BEmployerDataHub-Final/H1B-EmployerDataHub")
        print("  2. Click 'Crosstab View'")
        print("  3. Click Download > CSV")
        print("  4. Save as H1B_Employer_Data.csv in the h1b_enrichment folder")
        print("\nAlternatively, tell the agent: 'Download H-1B data and enrich with Hoovers'")
        sys.exit(1)

    print(f"Loaded: {len(rows)} rows")

    # Detect columns
    name_col, state_col = detect_columns(rows)
    print(f"Detected columns: name='{name_col}', state='{state_col}'")

    # Filter
    if args.california:
        print("\nFiltering: California (CA)")
        filtered = filter_by_state(rows, 'CA', name_col, state_col)
        output = args.output or str(CALIFORNIA_OUTPUT)
    elif args.all_us:
        print("\nProcessing: All US states")
        filtered = rows
        output = args.output or str(ALL_US_OUTPUT)
    else:
        print("\nNo filter specified. Use --california or --all-us")
        filtered = rows
        output = args.output or str(ALL_US_OUTPUT)

    # Deduplicate
    unique = deduplicate(filtered, name_col)
    print(f"After dedup: {len(unique)} unique employers")

    # Top N
    if args.top > 0:
        top = get_top_employers(unique, name_col, args.top)
        print(f"\nTop {args.top} employers by H-1B volume:")
        for i, (name, count) in enumerate(top, 1):
            print(f"  {i:3d}. {name[:60]:<60} ({count} petitions)")

        # Export top N
        top_names = set(n for n, c in top)
        top_rows = [r for r in unique if r.get(name_col, '').strip() in top_names]
        count = export_companies(top_rows, name_col, output)
        print(f"\nExported {count} rows to: {output}")
    else:
        count = export_companies(unique, name_col, output)
        print(f"\nExported {count} rows to: {output}")

    print("\nNext steps:")
    if args.california:
        print("  1. Tell agent: 'Enrich california_h1b_enriched.csv with Hoovers via CDP'")
    else:
        print("  1. Tell agent: 'Enrich all_us_h1b_enriched.csv with Hoovers via CDP'")


if __name__ == "__main__":
    main()
