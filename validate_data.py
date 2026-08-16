import pandas as pd
from pathlib import Path
BASE=Path(__file__).resolve().parent/"data"
C=["candidate_id","candidate_name","skills","accessibility_requirements","max_commute_km","preferred_work_mode","min_salary_lpa"]
J=["job_id","title","company","location","work_mode","commute_km","salary_lpa","required_skills","accessibility_features","flexibility_score","accessibility_score","workplace_support_score"]
for file, req in [("candidate_registry.csv",C),("job_registry.csv",J)]:
    df=pd.read_csv(BASE/file)
    missing=[x for x in req if x not in df.columns]
    print(f"{file}: {len(df)} rows | {'OK' if not missing else 'MISSING: '+', '.join(missing)}')
