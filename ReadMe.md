# Tech Talent Market Intelligence Hub
### An end-to-end data analytics product for understanding the technology job market

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)]()
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)]()
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow?logo=powerbi)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)]()

---

## The Problem
Companies and candidates make salary and hiring decisions without reliable, current 
market data. This project builds the intelligence layer that fixes that — using live 
job market data to answer:
- Which skills command the highest salary premium right now?
- Is it a candidate's market or employer's market?
- Which companies are aggressively hiring vs pulling back?

## What I Built

| Component | Technology | What it does |
|-----------|------------|--------------|
| Data Pipeline | Python (Scrapy) | Scrapes job postings from public sources |
| Analytics DB | PostgreSQL 15 | Star schema + 6 analytical queries |
| Dashboard | Power BI | 5-page interactive report with custom DAX measures |

## Key Findings
1. **Salary-Demand Inversion** — Falling-demand skills pay 20–35% above market (scarcity premium)
2. **The Senior Cliff** — Mid→Senior salary jump (~52%) is 2× larger than Entry→Mid (~26%)
3. **Remote Premium Reversed** — Remote roles now pay 8–12% *below* equivalent on-site (post-2024)
4. **COL-Adjusted Hidden Gems** — Austin and Raleigh offer 20%+ better purchasing power than SF/NYC

## Quick Start
```bash
git clone https://github.com/Ananyapkumar/tech-talent-market-intelligence-dashboard
cd tech-talent-intelligence
pip install -r requirements.txt
cp .env.example .env
python src/scraper/run_spider.py
psql -f src/db/schema.sql
python src/db/load_data.py
```

## Documentation
- [Executive Summary](docs/executive_summary.md)
- [Technical Documentation](docs/technical_documentation.md)
- [Architecture Diagram](docs/architecture_diagram.png)

## Dashboard Preview
![Executive Snapshot](docs/dashboard_screenshots/page1_executive.png)

---
*Built as a senior data analyst portfolio project demonstrating Python, SQL, and Power BI.*