# ♿ Accessible Job-Match Assistant

A privacy-conscious, local-first employment matching platform that connects candidates with job opportunities using skills, accessibility requirements, commute constraints, work modes, salary preferences, and workplace support features.

## What it provides

- 0–100 explainable job-match scoring
- Skill compatibility analysis
- Accessibility requirement coverage
- Commute compatibility
- Remote / Hybrid / On-site matching
- Salary preference matching
- Workplace support scoring
- Candidate profiles
- Opportunity discovery
- Factor-level match explanations
- Local CSV import and export
- Synthetic datasets for testing
- Input validation and data-quality controls
- Interactive Plotly analytics
- 100% local processing
- No external APIs
- No cloud database

## Dashboard

The application contains:

- **Match Studio** — personalized job recommendations
- **Opportunity Board** — filter and review available roles
- **Candidate Profiles** — inspect local candidate records
- **Match Explainer** — understand score factors
- **Data Lab** — safely replace local CSV datasets

## Technology

Python • Streamlit • Pandas • NumPy • Plotly • Local CSV Processing • Explainable Scoring • Accessibility Analytics

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 validate_data.py
python3 -m streamlit run app.py
```

Then open `http://localhost:8501`.

## Data

Synthetic demonstration datasets are included:

```text
data/candidate_registry.csv
data/job_registry.csv
```

Do not commit real candidate information or sensitive accommodation data to GitHub.

## Responsible use

This system is decision-support infrastructure, not an automated hiring decision-maker. Accessibility information should support workplace accommodations and job fit, not disability-based exclusion. Final recruitment decisions remain with appropriate human reviewers.

## License

MIT
