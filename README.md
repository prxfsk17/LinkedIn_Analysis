# LinkedIn Job Market Analysis (Warsaw)

A two-part project: a Selenium scraper that collects programming job postings from LinkedIn search results, and a Jupyter notebook that analyses the collected data (seniority, work format, employers, skills, applicants).

## Dataset

498 postings for Warsaw collected on 02.11.2026 using the search query "Software Engineer". For each posting: title, company, work format, employment type, seniority level, posted date, number of applicants, and boolean flags for ~90 technologies and skills found in the description.

The raw CSV is not included in the repository. The notebook keeps all its outputs, so the charts can be viewed directly on GitHub.

## Key findings

- **55% of postings do not state a seniority level.** Only about 9% explicitly target junior, entry-level or intern candidates; 27% are explicitly senior.
- **Hybrid (35%) and remote (30%) together make up about 65% of postings.**
- **79% of postings are full-time**; contract is 7%.
- **Python appears in 36% of postings**, Java in 27%, JavaScript in 21%; Docker, Kubernetes and AWS each in roughly a fifth.
- **About 46 applicants per posting** on average (approximate).
- **Most active employers in the sample:** Integral Solutions - Data & AI, Google, NVIDIA, BJAK.

See `analysis.ipynb` for the charts, the data quality notes and the full conclusions. Percentages are approximate: an earlier collection (March 2026) gave noticeably different shares.

## Project structure

```
.
├── main.py                  # entry point of the scraper
├── automating.py            # Selenium driver: login, paging, extraction
├── extractors.py            # work format, seniority and skill extraction
├── css_selectors.py         # page selectors
├── config.py, utils.py      # settings, CSV export
├── analysis.ipynb           # exploratory analysis and charts
├── requirements.txt         # scraper dependencies
└── requirements-analysis.txt
```

## Usage

Scraper (needs Chrome):

```bash
pip install -r requirements.txt
cp .env.example .env       # fill in URL, EMAIL, PASSWORD
python main.py
```

The browser opens the search page from `URL`, logs in, goes through the number of result pages set in `main.py` (`pages_quantity`) and writes `vacancies_warsaw.csv`.

Analysis:

```bash
pip install -r requirements-analysis.txt
jupyter notebook analysis.ipynb
```

## Limitations

- Skill, seniority and role-group detection is keyword-based and approximate; very short keywords (`go`, `r`) are overcounted and excluded from the charts.
- The results depend on the search query and on a single snapshot in time.
- Selectors depend on LinkedIn's current markup and may stop working; last verified on 02.11.2026.

## Roadmap
- [ ] Compare several snapshots over time

## Disclaimer

For educational purposes only. LinkedIn's terms restrict automated access; use at your own risk and do not publish scraped data.