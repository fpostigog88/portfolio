"""
H-1B Employer Data Enrichment Tool - Configuration
=================================================
Download H-1B data from: https://bigdataanalyticspub-sb.uscis.dhs.gov/views/H1BEmployerDataHub-Final/H1B-EmployerDataHub
Click "Crosstab View" → Download → CSV
Save as: H1B_Employer_Data.csv in this directory
"""

import os

# Directory for all enrichment files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Input CSV from USCIS (download manually from Tableau)
H1B_CSV_PATH = os.path.join(BASE_DIR, "H1B_Employer_Data.csv")

# Output files
CALIFORNIA_OUTPUT = os.path.join(BASE_DIR, "california_h1b_enriched.csv")
ALL_US_OUTPUT = os.path.join(BASE_DIR, "all_us_h1b_enriched.csv")

# Chrome CDP connection
CDP_HOST = "localhost"
CDP_PORT = 9522

# Enrichment settings
BATCH_SIZE = 10        # Companies per CDP batch
DELAY_BETWEEN_BATCHES = 2  # Seconds between batches (rate limit protection)
MAX_COMPANIES_PER_RUN = 500  # Max companies to enrich per run (avoid timeouts)

# Hoovers URLs
HOOVERS_BASE = "https://app.hoovers.dnb.com"
HOOVERS_SEARCH = f"{HOOVERS_BASE}/search/company"
HOOVERS_COMPANY = f"{HOOVERS_BASE}/company"

# State filter mapping (for Build a List)
US_STATE_CODES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming", "DC": "District of Columbia"
}
