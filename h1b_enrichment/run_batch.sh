#!/bin/bash
cd /c/Users/cadel/portfolio_public_clean/h1b_enrichment
python -u hoovers_scraper.py batch california_top500.txt 500 >> hoovers_enrichment_log.txt 2>&1
echo "DONE at $(date)" >> hoovers_enrichment_log.txt
