
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Accessible Job-Match Assistant", page_icon="♿", layout="wide")

st.markdown("""
<style>
.stApp{background:#f5f7fa;color:#17212b}.block-container{max-width:1480px;padding:1.25rem 2rem 3rem}
[data-testid="stSidebar"]{background:#fff;border-right:1px solid #e3e8ee}
[data-testid="stSidebar"] *{color:#17212b!important}
h1,h2,h3,h4{color:#17212b!important}
.hero{background:linear-gradient(135deg,#fff 0%,#f0f7ff 58%,#eefaf5 100%);border:1px solid #dfe7ef;border-radius:26px;padding:28px 32px;margin-bottom:20px;box-shadow:0 12px 34px rgba(20,35,55,.055)}
.hero-title{font-size:2rem;font-weight:850;letter-spacing:-.04em}.hero-sub{color:#617082;max-width:1000px;line-height:1.55;margin-top:7px}
.tag{display:inline-block;border-radius:999px;padding:5px 10px;margin:12px 5px 0 0;font-size:.72rem;font-weight:800}
.blue{background:#eaf3ff;color:#245d9c}.green{background:#eaf8f1;color:#147346}.purple{background:#f2edff;color:#6545a8}
.card{background:#fff;border:1px solid #dfe6ed;border-radius:18px;padding:18px 20px;box-shadow:0 7px 24px rgba(20,35,55,.04)}
.metric-label{color:#718096;text-transform:uppercase;font-size:.72rem;font-weight:800;letter-spacing:.06em}.metric-value{font-size:1.85rem;font-weight:850;color:#17212b;margin-top:3px}.metric-note{font-size:.77rem;color:#718096}
.section{font-size:1.15rem;font-weight:850;margin:20px 0 12px}.match{background:#fff;border:1px solid #dfe6ed;border-radius:18px;padding:17px 19px;margin-bottom:11px}.score{font-size:1.65rem;font-weight:900;color:#245d9c}
.pill{display:inline-block;background:#eef4fa;color:#35516e;border-radius:999px;padding:4px 9px;margin:5px 4px 0 0;font-size:.72rem;font-weight:800}.small{font-size:.78rem;color:#718096}
.ok{background:#eaf8f1;border:1px solid #bfe6cf;color:#176b42;padding:12px 14px;border-radius:12px}.warn{background:#fff8e8;border:1px solid #f2d69a;color:#78520a;padding:12px 14px;border-radius:12px}
.footer{text-align:center;color:#8290a0;font-size:.74rem;padding:30px}
</style>
""", unsafe_allow_html=True)

BASE=Path(__file__).resolve().parent
DATA=BASE/"data"; DATA.mkdir(exist_ok=True)
JOB_PATH=DATA/"job_registry.csv"; CAND_PATH=DATA/"candidate_registry.csv"

CAND_REQUIRED=["candidate_id","candidate_name","skills","accessibility_requirements","max_commute_km","preferred_work_mode","min_salary_lpa"]
JOB_REQUIRED=["job_id","title","company","location","work_mode","commute_km","salary_lpa","required_skills","accessibility_features","flexibility_score","accessibility_score","workplace_support_score"]
NUMERIC_CAND=["max_commute_km","min_salary_lpa"]
NUMERIC_JOB=["commute_km","salary_lpa","flexibility_score","accessibility_score","workplace_support_score"]

def sample_candidates(n=35,seed=19):
    rng=np.random.default_rng(seed); rows=[]
    for i in range(n):
        rows.append({"candidate_id":f"CAND-{2001+i}","candidate_name":f"Candidate {i+1:02d}",
        "skills":";".join(rng.choice(SKILLS,5,replace=False)),
        "accessibility_requirements":";".join(rng.choice(ACCESS,4,replace=False)),
        "max_commute_km":round(float(rng.uniform(4,30)),1),
        "preferred_work_mode":str(rng.choice(["Remote","Hybrid","On-site","Any"])),
        "min_salary_lpa":round(float(rng.uniform(3.5,9)),1)})
    return pd.DataFrame(rows)

def sample_jobs(n=100,seed=7):
    rng=np.random.default_rng(seed); rows=[]
    titles=["Data Analyst","Software Engineer","QA Analyst","Customer Support Specialist","Operations Associate","Documentation Specialist","Python Developer","Business Analyst","Technical Support Associate","Project Coordinator"]
    locations=["Pune","Mumbai","Bengaluru","Hyderabad","Chennai","Delhi","Remote"]
    for i in range(n):
        rows.append({"job_id":f"JOB-{1001+i}","title":str(rng.choice(titles)),"company":f"Accessible Employer {chr(65+i%26)}",
        "location":str(rng.choice(locations)),"work_mode":str(rng.choice(["Remote","Hybrid","On-site"],p=[.30,.45,.25])),
        "commute_km":round(float(rng.uniform(1,35)),1),"salary_lpa":round(float(rng.uniform(4,20)),1),
        "required_skills":";".join(rng.choice(SKILLS,4,replace=False)),
        "accessibility_features":";".join(rng.choice(ACCESS,6,replace=False)),
        "flexibility_score":int(rng.integers(50,101)),"accessibility_score":int(rng.integers(55,101)),
        "workplace_support_score":int(rng.integers(50,101))})
    return pd.DataFrame(rows)

def clean_columns(df):
    df=df.copy()
    df.columns=pd.Index(df.columns).astype(str).str.replace("\ufeff","",regex=False).str.strip()
    return df

def validate(df,required,numeric,name):
    if df is None or df.empty: raise ValueError(f"{name} is empty.")
    df=clean_columns(df)
    missing=[c for c in required if c not in df.columns]
    if missing: raise ValueError(f"{name} is missing required columns: {', '.join(missing)}")
    for col in numeric:
        df[col]=pd.to_numeric(df[col],errors="coerce")
        if df[col].isna().any(): raise ValueError(f"{name}: {col} contains blank or non-numeric values.")
    for col in required:
        if col not in numeric: df[col]=df[col].fillna("").astype(str).str.strip()
    idcol="candidate_id" if "candidate_id" in required else "job_id"
    if (df[idcol]=="").any(): raise ValueError(f"{name}: {idcol} contains blank values.")
    if df[idcol].duplicated().any(): raise ValueError(f"{name}: {idcol} contains duplicate IDs.")
    for col in ["flexibility_score","accessibility_score","workplace_support_score"]:
        if col in df and not df[col].between(0,100).all(): raise ValueError(f"{name}: {col} must be 0–100.")
    for col in ["max_commute_km","commute_km","salary_lpa","min_salary_lpa"]:
        if col in df and (df[col]<0).any(): raise ValueError(f"{name}: {col} cannot be negative.")
    return df

def load(path,required,numeric,name,factory):
    if not path.exists():
        df=factory(); df.to_csv(path,index=False); return df,None
    try: return validate(pd.read_csv(path),required,numeric,name),None
    except Exception as e: return factory(),str(e)

C,cerr=load(CAND_PATH,CAND_REQUIRED,NUMERIC_CAND,"Candidate dataset",sample_candidates)
J,jerr=load(JOB_PATH,JOB_REQUIRED,NUMERIC_JOB,"Job dataset",sample_jobs)

def vals(v):
    if pd.isna(v): return set()
    return {x.strip().lower() for x in str(v).split(";") if x.strip()}

def score(c,j):
    cs,js=vals(c["skills"]),vals(j["required_skills"]); needs,features=vals(c["accessibility_requirements"]),vals(j["accessibility_features"])
    skill=100*len(cs&js)/max(1,len(cs|js)); access=100*len(needs&features)/max(1,len(needs))
    commute=100 if c["max_commute_km"]>=j["commute_km"] else max(0,100-(j["commute_km"]-c["max_commute_km"])*8)
    pref,mode=str(c["preferred_work_mode"]),str(j["work_mode"])
    workmode=100 if pref=="Any" or pref==mode else (75 if {pref,mode}=={"Remote","Hybrid"} else 35)
    salary=100 if j["salary_lpa"]>=c["min_salary_lpa"] else max(0,100-(c["min_salary_lpa"]-j["salary_lpa"])*18)
    support=(float(j["accessibility_score"])+float(j["flexibility_score"])+float(j["workplace_support_score"]))/3
    total=.38*skill+.32*access+.12*commute+.06*workmode+.04*salary+.08*support
    return {"match_score":round(total),"skill_match":round(skill),"access_match":round(access),"commute_match":round(commute),"work_mode_match":round(workmode),"salary_match":round(salary),"workplace_support":round(support)}

def matches(c):
    rows=[]
    for _,j in J.iterrows():
        r=j.to_dict(); r.update(score(c,j)); rows.append(r)
    return pd.DataFrame(rows).sort_values(["match_score","access_match","skill_match"],ascending=False).reset_index(drop=True)

st.sidebar.markdown("## ♿ AccessMatch Local")
st.sidebar.caption("Accessible employment decision support")
st.sidebar.divider()
page=st.sidebar.radio("Workspace",["Match Studio","Opportunity Board","Candidate Profiles","Match Explainer","Data Lab"],label_visibility="collapsed")
st.sidebar.divider()
st.sidebar.markdown('<span class="tag green">LOCAL-FIRST</span><span class="tag blue">NO API</span><span class="tag purple">ACCESSIBILITY-AWARE</span>',unsafe_allow_html=True)
if cerr or jerr: st.sidebar.warning("A local CSV failed validation. Safe synthetic data is being used until it is corrected.")

st.markdown("""<div class="hero"><div class="hero-title">♿ Accessible Job-Match Assistant</div><div class="hero-sub">Local-first matching that connects candidates with jobs using skills, accessibility requirements, commute constraints, work modes, and workplace features — with transparent factor-level scoring.</div><span class="tag blue">SKILL MATCHING</span><span class="tag green">ACCESSIBILITY CONTEXT</span><span class="tag purple">EXPLAINABLE</span></div>""",unsafe_allow_html=True)

if page=="Match Studio":
    selected=st.selectbox("Candidate",C["candidate_id"].astype(str).tolist())
    threshold=st.slider("Minimum match score",0,100,60)
    row=C.loc[C["candidate_id"].astype(str)==selected]
    if row.empty: st.error("Candidate not found."); st.stop()
    c=row.iloc[0]; M=matches(c); shown=M[M["match_score"]>=threshold].head(10)
    cols=st.columns(4)
    metrics=[("Candidate",c["candidate_name"],c["preferred_work_mode"]),("Eligible matches",len(shown),"Above threshold"),("Best match",f'{M.iloc[0]["match_score"]}/100',"Transparent score"),("Access fit",f'{M.iloc[0]["access_match"]}%',"Requirement coverage")]
    for col,(a,b,d) in zip(cols,metrics): col.markdown(f'<div class="card"><div class="metric-label">{a}</div><div class="metric-value">{b}</div><div class="metric-note">{d}</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="section">Recommended opportunities</div>',unsafe_allow_html=True)
    if shown.empty: st.info("No matches meet the threshold. Lower the threshold to see closest matches.")
    for _,r in shown.iterrows():
        missing=sorted(vals(c["accessibility_requirements"])-vals(r["accessibility_features"]))
        review="All listed accessibility requirements are explicitly covered." if not missing else "Features not explicitly listed: "+", ".join(missing)
        st.markdown(f'<div class="match"><div style="display:flex;justify-content:space-between"><div><b>{r["title"]}</b> · {r["company"]}<br><span class="small">{r["location"]} • {r["work_mode"]} • {r["salary_lpa"]:.1f} LPA • {r["commute_km"]:.1f} km</span></div><div class="score">{r["match_score"]}/100</div></div><span class="pill">Skills {r["skill_match"]}%</span><span class="pill">Access {r["access_match"]}%</span><span class="pill">Commute {r["commute_match"]}%</span><span class="pill">Workplace {r["workplace_support"]}%</span><div class="small"><b>Review:</b> {review}</div></div>',unsafe_allow_html=True)

elif page=="Opportunity Board":
    st.markdown("### Opportunity Board")
    a,b,c,d=st.columns(4)
    with a: modes=st.multiselect("Work mode",["Remote","Hybrid","On-site"])
    with b: loc=st.multiselect("Location",sorted(J["location"].unique()))
    with c: minacc=st.slider("Minimum accessibility score",0,100,60)
    with d: maxkm=st.slider("Maximum commute (km)",1,40,30)
    V=J.copy()
    if modes: V=V[V["work_mode"].isin(modes)]
    if loc: V=V[V["location"].isin(loc)]
    V=V[(V["accessibility_score"]>=minacc)&(V["commute_km"]<=maxkm)]
    st.dataframe(V,use_container_width=True,hide_index=True)
    st.download_button("Export filtered opportunities",V.to_csv(index=False).encode(),"accessible_job_opportunities.csv","text/csv")

elif page=="Candidate Profiles":
    st.markdown("### Candidate Profiles"); st.dataframe(C,use_container_width=True,hide_index=True)
    st.download_button("Export candidate registry",C.to_csv(index=False).encode(),"candidate_registry.csv","text/csv")

elif page=="Match Explainer":
    cid=st.selectbox("Candidate",C["candidate_id"].astype(str).tolist(),key="explainer")
    c=C.loc[C["candidate_id"].astype(str)==cid].iloc[0]; m=matches(c).iloc[0]
    F=pd.DataFrame({"Factor":["Skill overlap","Accessibility coverage","Commute fit","Work-mode fit","Salary fit","Workplace support"],"Score":[m["skill_match"],m["access_match"],m["commute_match"],m["work_mode_match"],m["salary_match"],m["workplace_support"]]})
    l,r=st.columns(2)
    with l:
        fig=px.bar(F,x="Score",y="Factor",orientation="h",text="Score",range_x=[0,110],title="Match factor breakdown")
        fig.update_layout(height=420,paper_bgcolor="white",plot_bgcolor="#f8fafc")
        st.plotly_chart(fig,use_container_width=True)
    with r:
        st.markdown(f"### Best current match: {m['title']}"); st.metric("Overall match",f"{m['match_score']}/100")
        st.markdown(f'<div class="card"><b>{c["candidate_name"]}</b><br>{m["title"]} · {m["company"]}<br><br>The score combines skills, explicitly listed accessibility features, commute, work mode, salary preference, and workplace support.</div>',unsafe_allow_html=True)
        st.info("Accessibility requirements are workplace-fit and accommodation information, not disability-based exclusion criteria.")

else:
    st.markdown("### Data Lab")
    if cerr: st.markdown(f'<div class="warn"><b>Candidate CSV:</b> {cerr}</div>',unsafe_allow_html=True)
    else: st.markdown('<div class="ok">✓ Candidate CSV is valid.</div>',unsafe_allow_html=True)
    if jerr: st.markdown(f'<div class="warn"><b>Job CSV:</b> {jerr}</div>',unsafe_allow_html=True)
    else: st.markdown('<div class="ok">✓ Job CSV is valid.</div>',unsafe_allow_html=True)

    st.markdown("#### Candidate CSV — required columns"); st.code(", ".join(CAND_REQUIRED))
    u=st.file_uploader("Optional: replace local candidate dataset",type=["csv"],key="cand_upload")
    if u is not None:
        try:
            d=validate(pd.read_csv(u),CAND_REQUIRED,NUMERIC_CAND,"Uploaded candidate dataset")
            d.to_csv(CAND_PATH,index=False); st.success(f"Candidate dataset saved — {len(d)} records."); st.rerun()
        except Exception as e: st.error(f"Candidate CSV rejected: {e}")

    st.markdown("#### Job CSV — required columns"); st.code(", ".join(JOB_REQUIRED))
    u=st.file_uploader("Optional: replace local job dataset",type=["csv"],key="job_upload")
    if u is not None:
        try:
            d=validate(pd.read_csv(u),JOB_REQUIRED,NUMERIC_JOB,"Uploaded job dataset")
            d.to_csv(JOB_PATH,index=False); st.success(f"Job dataset saved — {len(d)} records."); st.rerun()
        except Exception as e: st.error(f"Job CSV rejected: {e}")

    a,b=st.columns(2); a.metric("Candidates",len(C)); b.metric("Jobs",len(J))
    st.info("Use consented, minimally necessary, appropriately anonymized data. This is decision-support software, not an automated hiring decision-maker.")

st.markdown('<div class="footer">Accessible Job-Match Assistant • 100% local Python processing • No external APIs • Accessibility-aware decision support</div>',unsafe_allow_html=True)
