"""Build the Kaggle HR attrition dashboard and its portfolio preview image."""

from __future__ import annotations

from html import escape
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SLUG = "hr-attrition-visualization"
PROJECT = ROOT / "projects" / SLUG
DATA = PROJECT / "data" / "ibm_hr_employee_attrition.csv"
COVER = ROOT / "assets" / "projects" / f"{SLUG}.jpg"
INCOME_SNAPSHOT = PROJECT / "assets" / "monthly_income_distribution.png"
KAGGLE_URL = "https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset"
ODBL_URL = "https://opendatacommons.org/licenses/odbl/1-0/"

NAVY = "#203447"
INK = "#172331"
CORAL = "#E66B5D"
TEAL = "#278A83"
BLUE = "#5D8FA3"
GOLD = "#D7A44A"
MIST = "#F3F6F7"
LINE = "#DCE4E7"
SATISFACTION = {1: "Low", 2: "Medium", 3: "High", 4: "Very High"}


def summarize(frame: pd.DataFrame, field: str, order: list[str] | None = None) -> pd.DataFrame:
    result = (
        frame.groupby(field, observed=True)
        .agg(
            Employees=("Attrition", "size"),
            EmployeesLeft=("Attrition", lambda values: int(values.eq("Yes").sum())),
        )
        .reset_index()
    )
    result["AttritionRatePct"] = result["EmployeesLeft"] / result["Employees"] * 100
    if order:
        result[field] = pd.Categorical(result[field], categories=order, ordered=True)
        result = result.sort_values(field)
        result[field] = result[field].astype(str)
    else:
        result = result.sort_values("AttritionRatePct", ascending=False)
    return result.reset_index(drop=True)


def styled(fig: go.Figure, height: int = 350) -> go.Figure:
    fig.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor="white",
        plot_bgcolor="#F7F9FA",
        font={"family": "Segoe UI, Arial, sans-serif", "color": NAVY, "size": 12},
        margin={"l": 48, "r": 24, "t": 28, "b": 48},
        legend={"orientation": "h", "y": 1.13, "x": 0},
        hoverlabel={"bgcolor": NAVY, "font": {"color": "white"}},
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E7ECEE", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#E7ECEE", zeroline=False)
    return fig


def make_dashboard(
    frame: pd.DataFrame,
    department: pd.DataFrame,
    roles: pd.DataFrame,
    satisfaction: pd.DataFrame,
    tenure: pd.DataFrame,
) -> None:
    employees = len(frame)
    left = int(frame["Attrition"].eq("Yes").sum())
    attrition_rate = left / employees * 100
    average_tenure = float(frame["YearsAtCompany"].mean())
    average_satisfaction = float(frame["JobSatisfaction"].mean())
    overtime_yes = frame["OverTime"].eq("Yes")
    overtime_no_rate = float(frame.loc[~overtime_yes, "Attrition"].eq("Yes").mean() * 100)
    overtime_yes_rate = float(frame.loc[overtime_yes, "Attrition"].eq("Yes").mean() * 100)

    metrics = [
        ("Employee records", f"{employees:,}", "Rows in the Kaggle sample"),
        ("Attrition rate", f"{attrition_rate:.1f}%", f"{left:,} records marked as left"),
        ("Average tenure", f"{average_tenure:.1f} years", "Years at company"),
        ("Job satisfaction", f"{average_satisfaction:.1f} / 4", "Average sample rating"),
    ]
    metric_html = "".join(
        f'<article class="metric"><span>{escape(label)}</span><strong>{escape(value)}</strong><small>{escape(detail)}</small></article>'
        for label, value, detail in metrics
    )

    dept_colors = [CORAL if index == 0 else TEAL for index in range(len(department))]
    fig_department = styled(go.Figure(), 340)
    fig_department.add_trace(
        go.Bar(
            x=department["AttritionRatePct"],
            y=department["Department"],
            orientation="h",
            marker_color=dept_colors,
            text=[f"{value:.1f}%" for value in department["AttritionRatePct"]],
            textposition="outside",
            cliponaxis=False,
            customdata=department[["Employees", "EmployeesLeft"]],
            hovertemplate="%{y}<br>Attrition rate: %{x:.1f}%<br>Records: %{customdata[0]}<br>Marked left: %{customdata[1]}<extra></extra>",
        )
    )
    fig_department.update_layout(
        showlegend=False,
        xaxis_title="Employees marked as left (%)",
        yaxis_title="",
        xaxis_range=[0, max(25, float(department["AttritionRatePct"].max()) * 1.35)],
        yaxis={"categoryorder": "array", "categoryarray": department["Department"].tolist(), "autorange": "reversed"},
    )

    overtime_share = pd.crosstab(frame["OverTime"], frame["Attrition"], normalize="index").mul(100)
    overtime_share = overtime_share.reindex(index=["No", "Yes"], columns=["No", "Yes"], fill_value=0)
    fig_overtime = styled(go.Figure(), 340)
    for status, label, color in (("No", "Stayed", TEAL), ("Yes", "Left", CORAL)):
        fig_overtime.add_trace(
            go.Bar(
                name=label,
                x=["No", "Yes"],
                y=overtime_share[status].tolist(),
                marker_color=color,
                hovertemplate="Overtime: %{x}<br>%{y:.1f}% %{fullData.name}<extra></extra>",
            )
        )
    fig_overtime.update_layout(barmode="stack", xaxis_title="Overtime reported", yaxis_title="Share of records (%)", yaxis_range=[0, 100], yaxis_ticksuffix="%")

    fig_roles = styled(go.Figure(), 445)
    fig_roles.add_trace(
        go.Bar(
            x=roles["AttritionRatePct"],
            y=roles["JobRole"],
            orientation="h",
            marker_color=[CORAL if value == roles["AttritionRatePct"].max() else BLUE for value in roles["AttritionRatePct"]],
            text=[f"{value:.1f}%" for value in roles["AttritionRatePct"]],
            textposition="outside",
            cliponaxis=False,
            customdata=roles[["Employees", "EmployeesLeft"]],
            hovertemplate="%{y}<br>Attrition rate: %{x:.1f}%<br>Records: %{customdata[0]}<br>Marked left: %{customdata[1]}<extra></extra>",
        )
    )
    fig_roles.update_layout(showlegend=False, xaxis_title="Employees marked as left (%)", yaxis_title="", xaxis_range=[0, max(45, float(roles["AttritionRatePct"].max()) * 1.22)], yaxis={"categoryorder": "array", "categoryarray": roles["JobRole"].tolist(), "autorange": "reversed"}, margin={"l": 150, "r": 30, "t": 28, "b": 48})

    fig_satisfaction = styled(go.Figure(), 340)
    fig_satisfaction.add_trace(
        go.Bar(
            x=satisfaction["Satisfaction"],
            y=satisfaction["AttritionRatePct"],
            marker_color=[CORAL, GOLD, BLUE, TEAL],
            text=[f"{value:.1f}%" for value in satisfaction["AttritionRatePct"]],
            textposition="outside",
            cliponaxis=False,
            customdata=satisfaction[["Employees", "EmployeesLeft"]],
            hovertemplate="Job satisfaction: %{x}<br>Attrition rate: %{y:.1f}%<br>Records: %{customdata[0]}<br>Marked left: %{customdata[1]}<extra></extra>",
        )
    )
    fig_satisfaction.update_layout(showlegend=False, xaxis_title="Self-reported job satisfaction", yaxis_title="Employees marked as left (%)", yaxis_range=[0, max(30, float(satisfaction["AttritionRatePct"].max()) * 1.25)])

    fig_tenure = styled(go.Figure(), 340)
    fig_tenure.add_trace(
        go.Bar(
            x=tenure["TenureBand"],
            y=tenure["AttritionRatePct"],
            marker_color=[CORAL if index == 0 else TEAL for index in range(len(tenure))],
            text=[f"{value:.1f}%" for value in tenure["AttritionRatePct"]],
            textposition="outside",
            cliponaxis=False,
            customdata=tenure[["Employees", "EmployeesLeft"]],
            hovertemplate="Tenure: %{x}<br>Attrition rate: %{y:.1f}%<br>Records: %{customdata[0]}<br>Marked left: %{customdata[1]}<extra></extra>",
        )
    )
    fig_tenure.update_layout(showlegend=False, xaxis_title="Years at company", yaxis_title="Employees marked as left (%)", yaxis_range=[0, max(30, float(tenure["AttritionRatePct"].max()) * 1.25)])

    fig_income = styled(go.Figure(), 340)
    for value, label, color in (("No", "Stayed", TEAL), ("Yes", "Left", CORAL)):
        values = frame.loc[frame["Attrition"].eq(value), "MonthlyIncome"]
        fig_income.add_trace(go.Box(y=values, name=label, marker_color=color, boxpoints="outliers", hovertemplate="%{x}<br>Monthly income: %{y:,.0f}<extra></extra>"))
    fig_income.update_layout(showlegend=False, xaxis_title="Attrition status", yaxis_title="Monthly income (dataset units)")

    charts = [
        ("Attrition by department", fig_department),
        ("Overtime and attrition mix", fig_overtime),
        ("Attrition by job role", fig_roles),
        ("Job satisfaction and attrition", fig_satisfaction),
        ("Attrition by company tenure", fig_tenure),
        ("Monthly income distribution", fig_income),
    ]
    chart_html = "".join(
        '<section class="chart-card"><h2>' + escape(title) + "</h2>"
        + pio.to_html(fig, full_html=False, include_plotlyjs="cdn", config={"responsive": True, "displayModeBar": False})
        + "</section>"
        for title, fig in charts
    )

    top_department = department.iloc[0]
    top_role = roles.iloc[0]
    low_satisfaction = satisfaction.iloc[0]
    observations = [
        f"{left:,} of {employees:,} records are marked as left ({attrition_rate:.1f}%).",
        f"{top_department['Department']} has the highest department rate in this sample at {top_department['AttritionRatePct']:.1f}% ({top_department['Employees']} records).",
        f"The overtime group shows {overtime_yes_rate:.1f}% attrition versus {overtime_no_rate:.1f}% without overtime; this is an association in a fictional dataset, not evidence of cause.",
        f"{top_role['JobRole']} has the highest job-role rate at {top_role['AttritionRatePct']:.1f}% ({top_role['Employees']} records), so compare group sizes alongside rates.",
        f"The low job-satisfaction group is at {low_satisfaction['AttritionRatePct']:.1f}%; ratings describe the sample and do not establish why employees left.",
    ]
    observation_html = "".join(f"<li>{escape(item)}</li>" for item in observations)
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Interactive visualization of the fictional IBM HR Analytics attrition dataset hosted on Kaggle.">
  <title>HR Workforce &amp; Attrition Visualization | Gift Sifwaku Project Lab</title>
  <style>
    :root {{ --navy:{NAVY}; --ink:{INK}; --coral:{CORAL}; --teal:{TEAL}; --mist:{MIST}; --line:{LINE}; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:var(--mist); color:var(--ink); font:15px/1.55 'Segoe UI',Arial,sans-serif; }}
    header {{ background:linear-gradient(120deg,#172b3a,var(--navy) 65%,#315a67); color:#fff; padding:42px 24px 48px; }}
    .wrap {{ width:min(1120px,calc(100% - 40px)); margin:0 auto; }}
    .eyebrow {{ color:#ffb2a7; font-size:.75rem; font-weight:700; letter-spacing:.16em; text-transform:uppercase; }}
    h1 {{ margin:10px 0 8px; font-size:clamp(2rem,4vw,3.4rem); line-height:1.05; letter-spacing:-.04em; }}
    header p {{ max-width:760px; color:#dce6e9; margin:0; }}
    .topline {{ display:flex; justify-content:space-between; align-items:center; gap:18px; margin-bottom:24px; }}
    .back {{ color:#fff; text-decoration:none; font-weight:700; }}
    .badge {{ border:1px solid rgba(255,255,255,.35); border-radius:99px; padding:7px 11px; color:#fff; font-size:.76rem; white-space:nowrap; }}
    .source {{ display:inline-block; margin-top:14px; color:#c7dbdf; font-size:.88rem; }}
    .source a {{ color:#fff; }}
    main {{ padding:26px 0 54px; }}
    .metrics {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; }}
    .metric {{ background:#fff; border:1px solid var(--line); border-radius:12px; padding:17px 18px; box-shadow:0 8px 24px rgba(32,52,71,.05); }}
    .metric span,.metric small {{ display:block; color:#60717d; }}
    .metric strong {{ display:block; color:var(--navy); font-size:1.7rem; letter-spacing:-.04em; margin:4px 0; }}
    .metric small {{ font-size:.75rem; }}
    .charts {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:14px; margin-top:15px; }}
    .chart-card {{ min-width:0; background:#fff; border:1px solid var(--line); border-radius:12px; padding:15px 13px 8px; box-shadow:0 8px 24px rgba(32,52,71,.04); }}
    .chart-card h2 {{ font-size:1rem; color:var(--navy); margin:0 8px; }}
    .insight {{ margin-top:15px; background:#fff; border:1px solid var(--line); border-left:4px solid var(--coral); border-radius:10px; padding:18px 20px; }}
    .insight h2 {{ margin:0 0 8px; color:var(--navy); font-size:1.1rem; }}
    .insight ul {{ margin:0; padding-left:20px; color:#526573; }}
    .insight li+li {{ margin-top:4px; }}
    .downloads {{ display:flex; flex-wrap:wrap; gap:10px; margin-top:17px; }}
    .downloads a {{ text-decoration:none; background:var(--navy); color:#fff; border-radius:7px; padding:10px 13px; font-size:.83rem; font-weight:700; }}
    .downloads a.secondary {{ background:#fff; color:var(--navy); border:1px solid var(--line); }}
    .notice {{ margin-top:15px; padding:15px 18px; border-radius:10px; background:#e8f0f0; color:#425b65; font-size:.88rem; }}
    .notice a {{ color:#1d625d; font-weight:700; }}
    footer {{ color:#637581; font-size:.78rem; padding:18px 0 28px; }}
    @media(max-width:760px) {{ .metrics {{ grid-template-columns:repeat(2,1fr); }} .charts {{ grid-template-columns:1fr; }} .topline {{ align-items:flex-start; flex-direction:column; }} }}
    @media(max-width:420px) {{ .wrap {{ width:min(1120px,calc(100% - 28px)); }} .metrics {{ gap:8px; }} .metric {{ padding:13px; }} .metric strong {{ font-size:1.35rem; }} }}
  </style>
</head>
<body>
  <header><div class="wrap">
    <div class="topline"><a class="back" href="../../index.html#projects">&#8592; Gift Sifwaku Portfolio</a><span class="badge">KAGGLE FICTIONAL DATASET</span></div>
    <div class="eyebrow">Project Lab / Data Visualization</div>
    <h1>HR Workforce &amp; Attrition Visualization</h1>
    <p>Explore how attrition rates vary across department, overtime, job role, satisfaction and tenure in the IBM HR sample.</p>
    <div class="source">Source: <a href="{KAGGLE_URL}" target="_blank" rel="noopener noreferrer">IBM HR Analytics Employee Attrition &amp; Performance on Kaggle</a></div>
  </div></header>
  <main class="wrap">
    <section class="metrics" aria-label="Dataset summary">{metric_html}</section>
    <section class="charts" id="chart-grid" aria-label="Interactive HR visualizations">{chart_html}</section>
    <section class="insight"><h2>What this sample shows</h2><ul>{observation_html}</ul>
      <div class="downloads"><a href="data/ibm_hr_employee_attrition.csv" download>Download Kaggle dataset</a><a class="secondary" href="data/department_attrition_summary.csv" download>Department summary</a><a class="secondary" href="data/job_role_attrition_summary.csv" download>Role summary</a><a class="secondary" href="README.md">Project notes</a></div>
    </section>
    <aside class="notice">Contains information from <a href="{KAGGLE_URL}" target="_blank" rel="noopener noreferrer">IBM HR Analytics Employee Attrition &amp; Performance</a>, made available under the <a href="{ODBL_URL}" target="_blank" rel="noopener noreferrer">Open Database License (ODbL)</a>. Kaggle describes the dataset as fictional; this is descriptive learning work, not a basis for employment decisions.</aside>
    <footer>Dataset source and license are credited above. Attrition patterns are descriptive associations; they do not explain individual decisions or prove causes.</footer>
  </main>
</body>
</html>"""
    (PROJECT / "dashboard.html").write_text(html, encoding="utf-8")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"]
        if bold
        else ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"]
    )
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def make_cover() -> None:
    width, height = 1600, 900
    image = Image.new("RGB", (width, height))
    pixels = image.load()
    top = (23, 39, 52)
    bottom = (37, 83, 91)
    for y in range(height):
        blend = y / (height - 1)
        row = tuple(round(top[i] * (1 - blend) + bottom[i] * blend) for i in range(3))
        for x in range(width):
            glow = max(0, 1 - abs(x - 1320) / 680) * 0.18
            pixels[x, y] = tuple(round(row[i] * (1 - glow) + (45, 110, 112)[i] * glow) for i in range(3))
    draw = ImageDraw.Draw(image, "RGBA")
    for x in range(0, width, 48):
        draw.line((x, 0, x, height), fill=(255, 255, 255, 14), width=1)
    for y in range(0, height, 48):
        draw.line((0, y, width, y), fill=(255, 255, 255, 14), width=1)
    draw.ellipse((970, -330, 1780, 480), fill=(255, 255, 255, 12))
    draw.ellipse((1140, 560, 1760, 1180), fill=(230, 107, 93, 18))

    draw.text((82, 82), "PROJECT 05  /  GIFT SIFWAKU", font=font(21, True), fill="#B6D1D4")
    draw.rounded_rectangle((82, 132, 160, 139), radius=3, fill=CORAL)
    for y, line in zip((190, 260, 330), ("HR Workforce", "Attrition", "Analysis")):
        draw.text((80, y), line, font=font(58, True), fill="#FFFFFF")
    draw.text((84, 433), "Visual patterns in a fictional", font=font(24), fill="#DCE8E9")
    draw.text((84, 468), "employee attrition dataset", font=font(24), fill="#DCE8E9")
    draw.rounded_rectangle((84, 755, 330, 804), radius=18, fill=CORAL)
    draw.text((105, 768), "INTERACTIVE DASHBOARD", font=font(16, True), fill="#FFFFFF")
    draw.text((84, 828), "KAGGLE DATASET  •  PYTHON VISUALIZATION", font=font(16, True), fill="#C1D6D8")

    stage = (755, 130, 1518, 755)
    draw.rounded_rectangle((stage[0] + 12, stage[1] + 15, stage[2] + 12, stage[3] + 15), radius=34, fill=(0, 0, 0, 48))
    draw.rounded_rectangle(stage, radius=32, fill=(248, 250, 250, 255))
    draw.text((805, 170), "PROJECT SNAPSHOT", font=font(18, True), fill=NAVY)
    draw.line((805, 214, 1468, 214), fill=LINE, width=2)
    chart_box = (790, 229, 1483, 724)
    draw.rounded_rectangle(chart_box, radius=17, fill="#F7F9FA", outline=LINE, width=2)
    with Image.open(INCOME_SNAPSHOT) as source:
        chart = source.convert("RGB")
        chart.thumbnail((670, 478), Image.Resampling.LANCZOS)
        chart_x = chart_box[0] + (chart_box[2] - chart_box[0] - chart.width) // 2
        chart_y = chart_box[1] + (chart_box[3] - chart_box[1] - chart.height) // 2
        image.paste(chart, (chart_x, chart_y))
    image.save(COVER, quality=92, optimize=True)


def main() -> None:
    if not DATA.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA}")
    if not INCOME_SNAPSHOT.exists():
        raise FileNotFoundError(f"Snapshot chart not found: {INCOME_SNAPSHOT}")
    frame = pd.read_csv(DATA)
    required = {"Attrition", "Department", "OverTime", "JobRole", "JobSatisfaction", "YearsAtCompany", "MonthlyIncome"}
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise ValueError(f"The Kaggle CSV is missing expected columns: {', '.join(missing)}")

    PROJECT.mkdir(parents=True, exist_ok=True)
    data_dir = PROJECT / "data"
    department = summarize(frame, "Department")
    roles = summarize(frame, "JobRole")
    frame["Satisfaction"] = frame["JobSatisfaction"].map(SATISFACTION)
    satisfaction = summarize(frame, "Satisfaction", ["Low", "Medium", "High", "Very High"])
    frame["TenureBand"] = pd.cut(
        frame["YearsAtCompany"],
        bins=[-1, 2, 5, 10, 100],
        labels=["0–2 years", "3–5 years", "6–10 years", "11+ years"],
    )
    tenure = summarize(frame, "TenureBand", ["0–2 years", "3–5 years", "6–10 years", "11+ years"])

    department.to_csv(data_dir / "department_attrition_summary.csv", index=False, float_format="%.2f")
    roles.to_csv(data_dir / "job_role_attrition_summary.csv", index=False, float_format="%.2f")
    satisfaction.to_csv(data_dir / "job_satisfaction_summary.csv", index=False, float_format="%.2f")
    tenure.to_csv(data_dir / "tenure_summary.csv", index=False, float_format="%.2f")
    make_dashboard(frame, department, roles, satisfaction, tenure)

    COVER.parent.mkdir(parents=True, exist_ok=True)
    make_cover()

    readme = f"""# HR Workforce & Attrition Visualization

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

Source: Pavan Subhasht, [IBM HR Analytics Employee Attrition & Performance on Kaggle]({KAGGLE_URL}). Kaggle describes the dataset as fictional data created by IBM data scientists. The Kaggle page lists the database license as Open Database and the contents license as Database Contents. The database is identified under the [Open Database License (ODbL) v1.0]({ODBL_URL}); the included source CSV and generated summaries are retained with source attribution.

The sample is not real employee data and is not representative of any actual employer. The dashboard shows descriptive associations only. It does not identify why an individual leaves, prove causes, or support hiring, promotion or other employment decisions.
"""
    (PROJECT / "README.md").write_text(readme, encoding="utf-8")

    license_note = f"""Dataset attribution: Pavan Subhasht, IBM HR Analytics Employee Attrition & Performance, Kaggle.
Dataset page: {KAGGLE_URL}
Kaggle license fields: Database: Open Database; Contents: Database Contents.
Database license URI: {ODBL_URL}

This folder contains the source CSV and aggregated summaries derived from it. Keep this attribution and license URI with redistributed copies. The Kaggle dataset description states that the data is fictional.
"""
    (data_dir / "DATA-LICENSE.txt").write_text(license_note, encoding="utf-8")
    print("Built the HR dashboard, four analysis summaries, and its portfolio snapshot from the Kaggle CSV.")


if __name__ == "__main__":
    main()
