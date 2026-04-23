# Technical Documentation

## Data Pipeline Architecture

### Extraction Layer (Python)
- **Spider:** Scrapy 2.11, targets RemoteOK public API
- **Rate limiting:** 2-second delay with ±50% randomisation, ROBOTSTXT_OBEY = True
- **Deduplication:** SHA256(title + company + date) generates a unique posting_id
- **Output:** Raw JSON (gitignored) + cleaned CSV in data/processed/

### Transformation Layer (SQL)
- **Database:** PostgreSQL 15, schema: talent
- **Tables:** 4 dimensions + 1 fact + 1 bridge = 6 total
- **Key design decisions:**
  - `salary_midpoint` is a GENERATED ALWAYS column — auto-computed, never stored incorrectly
  - `dim_dates` populated via GENERATE_SERIES for 2022–2026 (no calendar gaps)
  - Indexes added AFTER bulk load for faster insertion (then ANALYZE run)

### Analytics Queries

| File | Techniques Used | Business Purpose |
|------|----------------|-----------------|
| 01_skill_demand.sql | 3-level CTE, LAG(), RANK(), NTILE() | Demand ranking + MoM growth |
| 02_salary_analysis.sql | PERCENTILE_CONT, FIRST_VALUE, window frames | Salary distributions by level |
| 03_skill_salary_premium.sql | CROSS JOIN baseline, DENSE_RANK | Which skills pay more |
| 04_hiring_velocity.sql | Running SUM(), 4-week moving average | Company hiring signals |
| 05_geographic_salary.sql | COL-adjusted ranking, rank delta | Hidden gem cities |
| 06_skill_cooccurrence.sql | Self-join bridge table | Skill bundle analysis |

### Power BI Data Model
- **Connection:** PostgreSQL via native connector, Import Mode
- **Relationships:** Star schema mirrored exactly from SQL; bridge table uses bidirectional cross-filter
- **DAX Measures (3 custom):**
  - `Salary Percentile Context` — dynamic P25/P50/P75 with market premium signal (PERCENTILEX.INC + CALCULATETABLE)
  - `Skill Velocity Score` — composite 0–100 demand + growth score (RANKX + MAXX normalisation)
  - `Market Tightness Index` — candidate vs employer market signal (salary inflation + posting volume ratio)

---

## Reproducing the Results
```bash
# 1. Run the scraper
python src/scraper/run_spider.py

# 2. Create database schema
psql -U postgres -f src/db/schema.sql

# 3. Load data
python src/db/load_data.py

# 4. Run analytical queries (in DBeaver or psql)
psql -U postgres -d postgres -f src/db/queries/01_skill_demand.sql

# 5. Open Power BI
# File: powerbi/TechTalentHub.pbix
# Update connection: Transform Data → Data Source Settings → localhost:5432
```

---

## Known Limitations
1. Salary data relies on posted ranges — typically 10–20% higher than actual offers
2. Remote job geolocation defaults to "Worldwide" — COL analysis excludes these rows
3. Skill extraction uses tag matching, not NLP — may miss implicit skill requirements
4. RapidAPI free tier = 500 calls/month — salary enrichment may require multiple days

## Future Enhancements
- [ ] NLP skill extraction from job description text (spaCy or HuggingFace)
- [ ] Automated refresh pipeline via Apache Airflow DAGs
- [ ] LinkedIn API integration for actual hiring outcomes (not just postings)
- [ ] Predictive model: which skills will be top-demand in 6 months?
- [ ] Great Expectations integration for automated data quality checks