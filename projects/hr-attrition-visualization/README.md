# HR Workforce & Attrition Visualization

An interactive Python dashboard exploring employee attrition patterns across department, overtime, job role, job satisfaction and tenure.

## View and rebuild

Open `dashboard.html` in a browser. To rebuild the dashboard, aggregate CSV summaries and portfolio snapshot, run this from the repository root:

```bash
python -m pip install -r projects/requirements.txt
python projects/build_hr_visualization.py
```

## Files

- `data/ibm_hr_employee_attrition.csv` — source Kaggle CSV.
- `data/department_attrition_summary.csv` — counts and attrition rates by department.
- `data/job_role_attrition_summary.csv` — counts and attrition rates by job role.
- `data/job_satisfaction_summary.csv` — counts and attrition rates by satisfaction rating.
- `data/tenure_summary.csv` — counts and attrition rates by tenure band.
- `assets/monthly_income_distribution.png` — supplied chart shown in the portfolio snapshot.
- `dashboard.html` — interactive Plotly visualizations.

## Source, attribution and data note

Source: Pavan Subhasht, [IBM HR Analytics Employee Attrition & Performance on Kaggle](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset). Kaggle describes the dataset as fictional data created by IBM data scientists. The Kaggle page lists the database license as Open Database and the contents license as Database Contents. The database is identified under the [Open Database License (ODbL) v1.0](https://opendatacommons.org/licenses/odbl/1-0/); the included source CSV and generated summaries are retained with source attribution.

The sample is not real employee data and is not representative of any actual employer. The dashboard shows descriptive associations only. It does not identify why an individual leaves, prove causes, or support hiring, promotion or other employment decisions.
