# Recruitment & Hiring Analytics Dashboard

An interactive Streamlit dashboard for analyzing the end-to-end recruitment pipeline
(4,500 candidate records, Jan 2025–Jul 2026).

## Files in this folder
- `app.py` — the Streamlit dashboard (single file)
- `recruitment_clean.csv` — cleaned dataset used by the dashboard
- `requirements.txt` — Python packages needed to run it

## How to run it

1. Make sure `app.py` and `recruitment_clean.csv` are in the **same folder**.
2. Install the requirements (ideally in a virtual environment):

   ```bash
   pip install -r requirements.txt
   ```

3. Launch the dashboard:

   ```bash
   streamlit run app.py
   ```

4. Your browser will open automatically at `http://localhost:8501`.

> **Note:** This dashboard was built and code-reviewed in an environment without
> internet access to install Streamlit, so it could not be live-tested end-to-end here.
> The code follows standard, stable Streamlit/Plotly APIs — if you hit any error on
> your machine, it is most likely a package-version mismatch. Upgrading Streamlit
> (`pip install --upgrade streamlit`) resolves the vast majority of such issues,
> since the app uses `st.rerun()` and `multiselect(placeholder=...)`, which need
> Streamlit ≥ 1.27 (ideally ≥ 1.36).

## What's inside

### Filters (sidebar, apply to every page)
- Quick date-range buttons (All Time / Last 3, 6, 12 Months / Custom)
- Candidate Outcome buttons (All / Hired / Offer Declined / Rejected / In Pipeline)
- List-style multiselect filters: Department, Location, Recruitment Source, Job Role,
  Recruiter, Gender, Education Level

### Pages (top navigation, button style)
1. **Overview** — headline KPIs, monthly trend, applications by department/source/location, candidate status breakdown
2. **Recruitment Funnel** — funnel chart, stage-by-stage conversion, drop-off analysis, funnel by department/job role
3. **Source & Cost** — conversion & cost-per-hire by source, an efficiency bubble map, funnel by source
4. **Diversity** — gender/education/age/experience breakdowns and conversion rates
5. **Recruiter Performance** — per-recruiter volume, conversion, speed, and a summary table
6. **Quality of Hire** — interview/assessment scores (hired vs not hired), salary-gap analysis, decline reasons, probation outcomes
7. **Insights & Recommendations** — auto-recalculated insights based on your current filters, plus prioritized recommendations with reasoning

Every chart and KPI card recalculates live from the sidebar filters and page-level
outcome filter — nothing is hardcoded.

## Companion report
`Recruitment_Analytics_Report.docx` contains the same analysis in a formal written
report, with charts, a data-cleaning summary, and recommendations with reasoning.
