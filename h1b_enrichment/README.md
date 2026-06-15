# H-1B Employer + Hoovers Enrichment Tool

## What it does
Enriches H-1B employer data (from USCIS) with Hoovers company intelligence:
- Employees, revenue, city/state/country, Hoovers ID
- Data comes from Hoovers Redux globalSearch state (via Chrome CDP)

## Setup

### 1. Chrome CDP must be running
Your Chrome is already configured with CDP on port 9522.

### 2. You must be logged into Hoovers
The tool uses your existing Hoovers session. If session expires, log in again at app.hoovers.dnb.com

### 3. Install dependencies
```bash
pip install pandas
npm install ws   # for Node.js scripts
```

## Workflow

### Step 1: Download H-1B data from USCIS
1. Go to: https://bigdataanalyticspub-sb.uscis.dhs.gov/views/H1BEmployerDataHub-Final/H1B-EmployerDataHub
2. Click "Crosstab View"
3. Download > CSV
4. Save as `H1B_Employer_Data.csv` in this folder

### Step 2: Filter H-1B data
```bash
# California employers
python run_enrichment.py --california

# All US employers
python run_enrichment.py --all-us
```

### Step 3: Enrich with Hoovers
```bash
# Python (recommended)
python hoovers_scraper.py batch california_h1b_enriched.csv

# Node.js alternative
node hoovers_cdp.js batch california_h1b_enriched.txt
```

## Files

| File | Purpose |
|------|---------|
| `config.py` | Configuration |
| `run_enrichment.py` | Process H-1B CSV (filter, dedup) |
| `hoovers_scraper.py` | Python: Search + enrich via CDP |
| `hoovers_cdp.js` | Node.js: Search + enrich via CDP |

## Data extracted via Hoovers Redux

Each search returns:
- `companyName` - Full legal name
- `numEmployees` - Employee count
- `salesUsd` - Annual revenue in USD
- `city`, `stateName`, `countryName` - Address
- `hoovers_id` - Internal ID

Note: DUNS number is NOT available from search. To get DUNS, you need to visit the company profile page.

## Rate limits

- ~1-2 seconds between requests
- Session may expire after extended use (log in again if needed)
- Chrome must stay open with CDP enabled

## How it works (technical)

1. Navigate to Hoovers search page
2. Type in search input using React synthetic events (`nativeSetter` + `input.dispatchEvent`)
3. Redux `globalSearch.searchResults[]` is populated with company data
4. Extract companyName, numEmployees, salesUsd, addresses from Redux
