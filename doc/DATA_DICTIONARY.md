# Data Dictionary

## Candidate Registry

| Column | Description |
|---|---|
| candidate_id | Unique candidate identifier |
| candidate_name | Display name |
| skills | Semicolon-separated skills |
| accessibility_requirements | Semicolon-separated workplace/accessibility requirements |
| max_commute_km | Maximum preferred commute |
| preferred_work_mode | Remote, Hybrid, On-site, or Any |
| min_salary_lpa | Minimum salary preference |

## Job Registry

| Column | Description |
|---|---|
| job_id | Unique job identifier |
| title | Job title |
| company | Employer label |
| location | Job location |
| work_mode | Remote, Hybrid, or On-site |
| commute_km | Modeled commute distance |
| salary_lpa | Salary in LPA |
| required_skills | Semicolon-separated required skills |
| accessibility_features | Semicolon-separated workplace features |
| flexibility_score | 0–100 flexibility score |
| accessibility_score | 0–100 accessibility score |
| workplace_support_score | 0–100 workplace-support score |
