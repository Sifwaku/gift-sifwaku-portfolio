"""Build original Python project covers and reproducible demo dashboards.

All records generated here are synthetic examples. They are not real student,
shopping, wildlife-tracking, or pharmacy records.

Run from the portfolio root with:
    python projects/build_portfolio_demos.py
"""

from __future__ import annotations

from datetime import date, timedelta
from html import escape
from itertools import combinations
from math import asin, cos, radians, sin, sqrt
from pathlib import Path
import textwrap

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from PIL import Image, ImageDraw, ImageFont
from plotly.subplots import make_subplots


ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"
COVERS = ROOT / "assets" / "projects"

NAVY = "#203447"
INK = "#172331"
CORAL = "#E66B5D"
TEAL = "#278A83"
BLUE = "#5D8FA3"
GOLD = "#D7A44A"
MIST = "#F3F6F7"
LINE = "#DCE4E7"
PALETTE = [CORAL, TEAL, BLUE, GOLD, "#7A6CA8"]


def project_dir(slug: str) -> Path:
    path = PROJECTS / slug
    (path / "data").mkdir(parents=True, exist_ok=True)
    return path


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


def write_dashboard(
    slug: str,
    title: str,
    subtitle: str,
    metrics: list[tuple[str, str, str]],
    charts: list[tuple[str, go.Figure]],
    observations: list[str],
    data_file: str,
    extra_file: str,
    note: str,
) -> None:
    folder = project_dir(slug)
    metric_html = "".join(
        f'<article class="metric"><span>{escape(label)}</span>'
        f'<strong>{escape(value)}</strong><small>{escape(detail)}</small></article>'
        for label, value, detail in metrics
    )
    chart_html = "".join(
        '<section class="chart-card"><h2>' + escape(label) + "</h2>"
        + pio.to_html(
            fig,
            full_html=False,
            include_plotlyjs="cdn",
            config={"responsive": True, "displayModeBar": False},
        )
        + "</section>"
        for label, fig in charts
    )
    observation_html = "".join(f"<li>{escape(item)}</li>" for item in observations)
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} | Gift Sifwaku Project Lab</title>
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
    main {{ padding:26px 0 54px; }}
    .metrics {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-top:-2px; }}
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
    footer {{ color:#637581; font-size:.78rem; padding:18px 0 28px; }}
    @media(max-width:760px) {{ .metrics {{ grid-template-columns:repeat(2,1fr); }} .charts {{ grid-template-columns:1fr; }} .topline {{ align-items:flex-start; flex-direction:column; }} }}
    @media(max-width:420px) {{ .metrics {{ grid-template-columns:1fr 1fr; gap:8px; }} .metric {{ padding:13px; }} .metric strong {{ font-size:1.35rem; }} }}
  </style>
</head>
<body>
  <header><div class="wrap">
    <div class="topline"><a class="back" href="../../index.html#projects">&#8592; Gift Sifwaku Portfolio</a><span class="badge">SYNTHETIC DEMO DATA</span></div>
    <div class="eyebrow">Project Lab / Python Demonstration</div>
    <h1>{escape(title)}</h1>
    <p>{escape(subtitle)}</p>
  </div></header>
  <main class="wrap">
    <section class="metrics" aria-label="Project summary">{metric_html}</section>
    <section class="charts" aria-label="Interactive charts">{chart_html}</section>
    <section class="insight"><h2>What this demo shows</h2><ul>{observation_html}</ul>
      <div class="downloads"><a href="data/{escape(data_file)}" download>Download sample data</a><a class="secondary" href="data/{escape(extra_file)}" download>Download analysis output</a><a class="secondary" href="README.md">Project notes</a></div>
    </section>
    <footer>{escape(note)}</footer>
  </main>
</body>
</html>"""
    (folder / "dashboard.html").write_text(html, encoding="utf-8")


def write_readme(slug: str, title: str, summary: str, run_file: str, files: str, note: str) -> None:
    folder = project_dir(slug)
    readme = f"""# {title}

{summary}

## Run the demo

From the portfolio repository root:

```bash
python -m pip install -r projects/requirements.txt
python projects/build_portfolio_demos.py
```

The script writes its synthetic input data and analysis outputs into this project folder. Open `dashboard.html` in a browser to explore the charts.

## Files

{files}

## Data note

{note}
"""
    (folder / "README.md").write_text(readme, encoding="utf-8")


def generate_student_performance() -> None:
    slug = "student-performance-analysis"
    folder = project_dir(slug)
    rng = np.random.default_rng(2026)
    n = 280
    study_hours = np.clip(rng.normal(3.4, 1.25, n), 0.3, 8.0)
    attendance = np.clip(63 + study_hours * 4.2 + rng.normal(0, 8, n), 42, 100)
    assignments = np.clip(54 + study_hours * 5.0 + rng.normal(0, 12, n), 20, 100)
    sleep = np.clip(rng.normal(7.0, 1.05, n), 4.0, 10.0)
    score = np.clip(
        22 + study_hours * 5.3 + (attendance - 70) * 0.22
        + (assignments - 60) * 0.16 + (sleep - 7) * 1.2
        + rng.normal(0, 8.3, n),
        18,
        100,
    )
    df = pd.DataFrame(
        {
            "student_id": [f"S{i:03d}" for i in range(1, n + 1)],
            "weekly_study_hours": study_hours.round(1),
            "attendance_pct": attendance.round(1),
            "assignment_completion_pct": assignments.round(1),
            "sleep_hours": sleep.round(1),
            "final_score_pct": score.round(1),
        }
    )
    df["performance_band"] = pd.cut(
        df["final_score_pct"],
        bins=[0, 49.9, 64.9, 79.9, 100],
        labels=["Needs support", "Developing", "Proficient", "Strong"],
    ).astype(str)
    df.to_csv(folder / "data" / "sample_students.csv", index=False)

    avg = float(df.final_score_pct.mean())
    pass_rate = float((df.final_score_pct >= 50).mean() * 100)
    attendance_mean = float(df.attendance_pct.mean())
    fig1 = styled(go.Figure())
    fig1.add_trace(
        go.Histogram(
            x=df.final_score_pct,
            nbinsx=18,
            marker={"color": TEAL, "line": {"color": "white", "width": 1}},
            hovertemplate="Score: %{x:.0f}%<br>Students: %{y}<extra></extra>",
        )
    )
    fig1.add_vline(x=50, line_dash="dash", line_color=CORAL, annotation_text="Pass mark")
    fig1.update_layout(xaxis_title="Final score (%)", yaxis_title="Students", showlegend=False)

    fig2 = styled(go.Figure())
    fig2.add_trace(
        go.Scatter(
            x=df.weekly_study_hours,
            y=df.final_score_pct,
            mode="markers",
            name="Learners",
            marker={"size": 8, "color": df.attendance_pct, "colorscale": [[0, BLUE], [1, CORAL]], "showscale": True, "colorbar": {"title": "Attendance %"}, "opacity": 0.78},
            hovertemplate="Study time: %{x:.1f} h/week<br>Final score: %{y:.1f}%<extra></extra>",
        )
    )
    xfit = np.linspace(float(df.weekly_study_hours.min()), float(df.weekly_study_hours.max()), 40)
    slope, intercept = np.polyfit(df.weekly_study_hours, df.final_score_pct, 1)
    fig2.add_trace(go.Scatter(x=xfit, y=slope * xfit + intercept, mode="lines", name="Linear trend", line={"color": NAVY, "width": 3}))
    fig2.update_layout(xaxis_title="Weekly study hours", yaxis_title="Final score (%)")

    band = df.groupby("performance_band", observed=False).final_score_pct.agg(["mean", "count"]).reindex(
        ["Needs support", "Developing", "Proficient", "Strong"]
    )
    fig3 = styled(go.Figure())
    fig3.add_trace(go.Bar(x=band.index.astype(str), y=band["mean"], marker_color=[CORAL, GOLD, BLUE, TEAL], text=band["count"], texttemplate="n=%{text}", textposition="outside", hovertemplate="%{x}<br>Average: %{y:.1f}%<extra></extra>"))
    fig3.update_layout(xaxis_title="Score band", yaxis_title="Average score (%)", yaxis_range=[0, 105], showlegend=False)

    features = ["weekly_study_hours", "attendance_pct", "assignment_completion_pct", "sleep_hours", "final_score_pct"]
    corr = df[features].corr()
    fig4 = styled(go.Figure())
    fig4.add_trace(go.Heatmap(z=corr.values, x=[x.replace("_", " ").title() for x in features], y=[x.replace("_", " ").title() for x in features], zmin=-1, zmax=1, colorscale=[[0, BLUE], [0.5, "#FFFFFF"], [1, CORAL]], text=np.round(corr.values, 2), texttemplate="%{text:.2f}", hovertemplate="%{y} × %{x}: %{z:.2f}<extra></extra>"))
    fig4.update_layout(height=390, margin={"l": 130, "r": 20, "t": 25, "b": 100})

    summary = (
        df.groupby("performance_band", observed=False)
        .agg(students=("student_id", "count"), average_score=("final_score_pct", "mean"), average_study_hours=("weekly_study_hours", "mean"))
        .round(2)
        .reset_index()
    )
    summary.to_csv(folder / "data" / "performance_summary.csv", index=False)
    write_dashboard(
        slug,
        "Student Performance Analysis",
        "A compact exploratory analysis of study habits, attendance, assignment completion and final scores.",
        [("Learners", f"{n:,}", "Synthetic sample"), ("Mean score", f"{avg:.1f}%", "Across this sample"), ("Pass rate", f"{pass_rate:.1f}%", "Score at or above 50%"), ("Mean attendance", f"{attendance_mean:.1f}%", "Across this sample")],
        [("Score distribution", fig1), ("Study time and final score", fig2), ("Average score by band", fig3), ("Feature relationships", fig4)],
        [
            "The sample has a positive association between weekly study time and final score.",
            "Attendance and assignment completion also vary with score in this generated example.",
            "These patterns describe synthetic data and do not establish cause and effect.",
        ],
        "sample_students.csv",
        "performance_summary.csv",
        "Demonstration only: every learner record in this dashboard was generated by this script. It is not real student data.",
    )
    write_readme(slug, "Student Performance Analysis", "A reproducible exploratory-data-analysis demo built with Python, pandas, NumPy and Plotly.", "analyze.py", "- `data/sample_students.csv` — generated learner sample.\n- `data/performance_summary.csv` — score-band summary.\n- `dashboard.html` — interactive report.", "All learner records are synthetic examples. Replace them only with data you are permitted to use, and protect student privacy.")


def generate_market_basket() -> None:
    slug = "market-basket-analysis"
    folder = project_dir(slug)
    rng = np.random.default_rng(441)
    archetypes = [
        ({"coffee", "bread", "milk"}, 0.30),
        ({"tea", "sugar", "lemon"}, 0.23),
        ({"pasta", "tomato sauce", "cheese"}, 0.21),
        ({"diapers", "wipes", "baby lotion"}, 0.14),
        ({"oats", "yogurt", "berries"}, 0.12),
    ]
    staple_items = ["rice", "bananas", "eggs", "water"]
    transactions: list[set[str]] = []
    rows: list[dict[str, str]] = []
    for index in range(1, 521):
        choice = int(rng.choice(len(archetypes), p=[w for _, w in archetypes]))
        basket = set(archetypes[choice][0])
        for item in staple_items:
            if rng.random() < 0.11:
                basket.add(item)
        if rng.random() < 0.08:
            basket.add("chocolate")
        transactions.append(basket)
        rows.extend({"transaction_id": f"T{index:04d}", "item": item} for item in sorted(basket))
    pd.DataFrame(rows).to_csv(folder / "data" / "sample_basket_items.csv", index=False)

    universe = sorted(set().union(*transactions))
    n = len(transactions)
    support_count: dict[tuple[str, ...], int] = {}
    for size in (1, 2, 3):
        for combo in combinations(universe, size):
            support_count[combo] = sum(set(combo).issubset(basket) for basket in transactions)
    item_support = {item: support_count[(item,)] / n for item in universe}
    rules: list[dict[str, float | str | int]] = []
    for itemset, joint_count in support_count.items():
        if len(itemset) < 2 or joint_count < n * 0.035:
            continue
        for left_size in range(1, len(itemset)):
            for left in combinations(itemset, left_size):
                right = tuple(item for item in itemset if item not in left)
                left_count = support_count.get(tuple(sorted(left)), 0)
                right_count = support_count.get(tuple(sorted(right)), 0)
                if not left_count or not right_count:
                    continue
                support = joint_count / n
                confidence = joint_count / left_count
                lift = confidence / (right_count / n)
                if confidence < 0.25:
                    continue
                rules.append(
                    {
                        "antecedent": " + ".join(left),
                        "consequent": " + ".join(right),
                        "support": support,
                        "confidence": confidence,
                        "lift": lift,
                        "transaction_count": joint_count,
                    }
                )
    rules_df = pd.DataFrame(rules).drop_duplicates(subset=["antecedent", "consequent"])
    if not rules_df.empty:
        rules_df = rules_df.sort_values(["lift", "support"], ascending=[False, False]).reset_index(drop=True)
    rules_df.to_csv(folder / "data" / "association_rules.csv", index=False, float_format="%.4f")

    top_items = sorted(item_support.items(), key=lambda item: item[1], reverse=True)[:12]
    fig1 = styled(go.Figure())
    fig1.add_trace(go.Bar(x=[value * 100 for _, value in top_items], y=[item.title() for item, _ in top_items], orientation="h", marker_color=TEAL, hovertemplate="%{y}<br>Basket support: %{x:.1f}%<extra></extra>"))
    fig1.update_layout(yaxis={"categoryorder": "total ascending"}, xaxis_title="Transactions containing item (%)", showlegend=False)

    top_rules = rules_df.head(10).copy()
    labels = (top_rules.antecedent + "  →  " + top_rules.consequent).tolist() if not top_rules.empty else []
    fig2 = styled(go.Figure())
    fig2.add_trace(go.Bar(x=top_rules.lift, y=labels, orientation="h", marker={"color": top_rules.support, "colorscale": [[0, BLUE], [1, CORAL]], "showscale": True, "colorbar": {"title": "Support"}}, hovertemplate="Lift: %{x:.2f}<br>%{y}<extra></extra>"))
    fig2.update_layout(yaxis={"categoryorder": "total ascending"}, xaxis_title="Lift (higher means stronger association)", showlegend=False)

    pair = pd.DataFrame(index=universe, columns=universe, dtype=float)
    for a, b in combinations(universe, 2):
        sup_ab = support_count[tuple(sorted((a, b)))] / n
        value = sup_ab / (item_support[a] * item_support[b]) if item_support[a] and item_support[b] else 0
        pair.loc[a, b] = value
        pair.loc[b, a] = value
    pair_values = pair.fillna(0).astype(float)
    fig3 = styled(go.Figure())
    fig3.add_trace(go.Heatmap(z=pair_values.values, x=[x.title() for x in universe], y=[x.title() for x in universe], colorscale=[[0, "#F3F6F7"], [0.5, BLUE], [1, CORAL]], colorbar={"title": "Pair lift"}, hovertemplate="%{y} + %{x}<br>Pair lift: %{z:.2f}<extra></extra>"))
    fig3.update_layout(height=480, margin={"l": 115, "r": 25, "t": 25, "b": 120})

    strongest_lift = float(rules_df.lift.max()) if not rules_df.empty else 0.0
    metrics = [
        ("Transactions", f"{n:,}", "Synthetic baskets"),
        ("Products", str(len(universe)), "Distinct sample items"),
        ("Rules found", f"{len(rules_df):,}", "At 3.5% support / 25% confidence"),
        ("Highest lift", f"{strongest_lift:.2f}", "In this generated sample"),
    ]
    write_dashboard(
        slug,
        "Market Basket Analysis",
        "Association-rule mining over generated shopping baskets, with support, confidence and lift made easy to compare.",
        metrics,
        [("Most common items", fig1), ("Strongest sample rules", fig2), ("Pair association map", fig3)],
        [
            "Support measures how often an item set appears in the sample.",
            "Confidence measures how often the consequent appears when the antecedent appears.",
            "Lift compares a rule with the consequent's baseline frequency; lift above 1 is a positive association in this sample.",
        ],
        "sample_basket_items.csv",
        "association_rules.csv",
        "Demonstration only: these generated transactions do not describe real shoppers, sales, or purchasing recommendations.",
    )
    write_readme(slug, "Market Basket Analysis", "A small, transparent Apriori-style association-rule demo using Python, pandas, NumPy and Plotly.", "analyze.py", "- `data/sample_basket_items.csv` — generated transaction-item rows.\n- `data/association_rules.csv` — mined rules with support, confidence and lift.\n- `dashboard.html` — interactive report.", "Every basket is synthetic and generated with known example patterns so the calculations can be explored. The results are not real retail findings.")


def haversine_km(lat1: np.ndarray, lon1: np.ndarray, lat2: np.ndarray, lon2: np.ndarray) -> np.ndarray:
    earth = 6371.0
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dp = p2 - p1
    dl = np.radians(lon2 - lon1)
    a = np.sin(dp / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * earth * np.arcsin(np.sqrt(a))


def generate_bird_tracking() -> None:
    slug = "bird-migration-tracking"
    folder = project_dir(slug)
    rng = np.random.default_rng(809)
    waypoints = np.array(
        [
            [-15.42, 28.28],
            [-14.93, 28.55],
            [-14.45, 28.90],
            [-13.98, 29.24],
            [-13.48, 29.62],
            [-13.03, 30.02],
            [-12.60, 30.44],
        ]
    )
    points = []
    for start, end in zip(waypoints[:-1], waypoints[1:]):
        for fraction in np.linspace(0, 1, 20, endpoint=False):
            points.append(start + (end - start) * fraction)
    points.append(waypoints[-1])
    route = np.asarray(points) + rng.normal(0, 0.018, (len(points), 2))
    n = len(route)
    timestamps = pd.date_range("2026-10-01 06:00", periods=n, freq="6h")
    progress = np.linspace(0, 1, n)
    battery = np.clip(98 - progress * 31 + rng.normal(0, 1.2, n), 55, 100)
    rssi = np.clip(-63 - 24 * np.abs(np.sin(np.linspace(0, 4 * np.pi, n))) + rng.normal(0, 4, n), -105, -50)
    altitude = np.clip(840 + 130 * np.sin(np.linspace(0, 3 * np.pi, n)) + rng.normal(0, 35, n), 650, 1100)
    distance = haversine_km(route[:-1, 0], route[:-1, 1], route[1:, 0], route[1:, 1])
    cumulative = np.concatenate([[0], np.cumsum(distance)])
    df = pd.DataFrame(
        {
            "timestamp_utc": timestamps.astype(str),
            "tag_id": "SIM-001",
            "latitude": route[:, 0].round(5),
            "longitude": route[:, 1].round(5),
            "estimated_altitude_m": altitude.round(1),
            "battery_pct": battery.round(1),
            "signal_dbm": rssi.round(1),
            "cumulative_distance_km": cumulative.round(2),
        }
    )
    df.to_csv(folder / "data" / "sample_telemetry.csv", index=False)

    fig1 = styled(go.Figure(), 390)
    fig1.add_trace(go.Scatter(x=df.longitude, y=df.latitude, mode="lines+markers", line={"color": TEAL, "width": 3}, marker={"size": 7, "color": np.arange(n), "colorscale": [[0, CORAL], [1, BLUE]], "showscale": True, "colorbar": {"title": "Fix #"}}, customdata=np.column_stack([df.timestamp_utc, df.battery_pct]), hovertemplate="Lon: %{x:.4f}<br>Lat: %{y:.4f}<br>Time: %{customdata[0]}<br>Battery: %{customdata[1]:.0f}%<extra></extra>"))
    fig1.add_trace(go.Scatter(x=[df.longitude.iloc[0]], y=[df.latitude.iloc[0]], mode="markers+text", name="Start", marker={"size": 14, "color": CORAL, "symbol": "circle"}, text=["START"], textposition="top center"))
    fig1.add_trace(go.Scatter(x=[df.longitude.iloc[-1]], y=[df.latitude.iloc[-1]], mode="markers+text", name="Latest", marker={"size": 14, "color": NAVY, "symbol": "diamond"}, text=["LATEST"], textposition="top center"))
    fig1.update_layout(xaxis_title="Longitude (°)", yaxis_title="Latitude (°)", yaxis_scaleanchor="x", yaxis_scaleratio=1)

    fig2 = styled(go.Figure())
    fig2.add_trace(go.Scatter(x=df.timestamp_utc, y=df.battery_pct, mode="lines", fill="tozeroy", line={"color": CORAL, "width": 3}, fillcolor="rgba(230,107,93,.12)", hovertemplate="%{x}<br>Battery: %{y:.1f}%<extra></extra>"))
    fig2.update_layout(xaxis_title="Telemetry time (UTC)", yaxis_title="Battery remaining (%)", yaxis_range=[0, 105])

    fig3 = styled(go.Figure())
    fig3.add_trace(go.Scatter(x=df.cumulative_distance_km, y=df.signal_dbm, mode="markers", marker={"size": 9, "color": df.estimated_altitude_m, "colorscale": [[0, BLUE], [1, GOLD]], "showscale": True, "colorbar": {"title": "Altitude m"}}, hovertemplate="Distance: %{x:.1f} km<br>Signal: %{y:.0f} dBm<extra></extra>"))
    fig3.add_hline(y=-90, line_dash="dash", line_color=CORAL, annotation_text="Weak-signal guide")
    fig3.update_layout(xaxis_title="Cumulative demo distance (km)", yaxis_title="Signal strength (dBm)")

    total = float(cumulative[-1])
    metrics = [
        ("GPS fixes", str(n), "Generated telemetry points"),
        ("Demo distance", f"{total:.1f} km", "Approximate from sample coordinates"),
        ("Latest battery", f"{battery[-1]:.0f}%", "Simulated tag reading"),
        ("Mean signal", f"{rssi.mean():.0f} dBm", "Across generated points"),
    ]
    write_dashboard(
        slug,
        "Bird Migration Tracking System",
        "A Python telemetry prototype showing how GPS fixes, tag battery and radio-signal readings could be inspected.",
        metrics,
        [("Simulated telemetry route", fig1), ("Tag battery over time", fig2), ("Radio signal by distance", fig3)],
        [
            "The track is generated for a dashboard prototype and is not a real bird route.",
            "Battery and signal readings are synthetic examples for monitoring-interface design.",
            "A deployed tracker would need validated hardware, field testing, animal-welfare review and real location data.",
        ],
        "sample_telemetry.csv",
        "sample_telemetry.csv",
        "Prototype simulation only: the coordinates do not represent a tagged animal or a confirmed migration path.",
    )
    write_readme(slug, "Bird Migration Tracking System", "A simulated Python telemetry dashboard supporting the portfolio's ESP32 / LoRa / Wi-Fi system concept.", "simulate.py", "- `data/sample_telemetry.csv` — generated GPS and tag-health readings.\n- `dashboard.html` — route and device-health visualizations.", "Coordinates and sensor values are synthetic. This demo is not wildlife research and does not claim a real migration route.")


def generate_pharmacy_inventory() -> None:
    slug = "pharmacy-inventory-alert"
    folder = project_dir(slug)
    rng = np.random.default_rng(163)
    products = [
        ("Oral hydration sachets", "Wellness"), ("Elastic bandage", "First aid"),
        ("Digital thermometer", "Devices"), ("Vitamin C tablets", "Wellness"),
        ("Surgical masks", "Protection"), ("Adhesive dressings", "First aid"),
        ("Hand sanitizer", "Protection"), ("Cotton wool pack", "First aid"),
        ("Disposable gloves", "Protection"), ("Saline solution", "Care"),
        ("Gauze pads", "First aid"), ("Pill organizer", "Devices"),
        ("Zinc tablets", "Wellness"), ("Antiseptic wipes", "Care"),
        ("Ice pack", "Devices"), ("Medical tape", "First aid"),
        ("Face shields", "Protection"), ("Digital scale", "Devices"),
        ("Calcium tablets", "Wellness"), ("Wound cleanser", "Care"),
        ("Bandage scissors", "Devices"), ("Disposable aprons", "Protection"),
        ("Hot water bottle", "Devices"), ("Lens wipes", "Care"),
        ("First aid kit", "First aid"), ("Electrolyte drink mix", "Wellness"),
        ("Protective eyewear", "Protection"), ("Measuring cup", "Devices"),
        ("Moisturizing cream", "Care"), ("Paper tape", "First aid"),
        ("Reusable cold pack", "Devices"), ("Oral care rinse", "Care"),
        ("Multivitamin tablets", "Wellness"), ("Protective gowns", "Protection"),
        ("Compress pads", "First aid"), ("Cleaning swabs", "Care"),
    ]
    today = date(2026, 11, 6)
    rows = []
    for i, (name, category) in enumerate(products, start=1):
        reorder = int(rng.integers(12, 38))
        stock = int(rng.integers(0, 72))
        cost = float(rng.uniform(1.5, 28.0))
        days = int(rng.integers(8, 420))
        status = "Urgent reorder" if stock < reorder * 0.45 else "Reorder" if stock < reorder else "In stock"
        rows.append(
            {
                "sku": f"DEMO-{i:03d}",
                "product": name,
                "category": category,
                "quantity_on_hand": stock,
                "reorder_level": reorder,
                "unit_cost_demo": round(cost, 2),
                "stock_value_demo": round(stock * cost, 2),
                "expiry_date_demo": (today + timedelta(days=days)).isoformat(),
                "days_to_expiry_demo": days,
                "status_demo": status,
            }
        )
    df = pd.DataFrame(rows).sort_values(["status_demo", "quantity_on_hand"])
    df.to_csv(folder / "data" / "sample_inventory.csv", index=False)
    alerts = df[(df.status_demo != "In stock") | (df.days_to_expiry_demo <= 60)].copy()
    alerts.to_csv(folder / "data" / "sample_alerts.csv", index=False)

    order = ["Urgent reorder", "Reorder", "In stock"]
    status_counts = df.status_demo.value_counts().reindex(order, fill_value=0)
    fig1 = styled(go.Figure())
    fig1.add_trace(go.Bar(x=status_counts.index, y=status_counts.values, marker_color=[CORAL, GOLD, TEAL], text=status_counts.values, textposition="outside", hovertemplate="%{x}<br>Products: %{y}<extra></extra>"))
    fig1.update_layout(yaxis_title="Products", showlegend=False)

    low = df.nsmallest(14, "quantity_on_hand").sort_values("quantity_on_hand")
    fig2 = styled(go.Figure(), 420)
    fig2.add_trace(go.Bar(x=low.quantity_on_hand, y=low["product"], orientation="h", name="On hand", marker_color=TEAL, hovertemplate="%{y}<br>On hand: %{x}<extra></extra>"))
    fig2.add_trace(go.Scatter(x=low.reorder_level, y=low["product"], mode="markers", name="Reorder level", marker={"color": CORAL, "size": 11, "symbol": "line-ew"}, hovertemplate="%{y}<br>Reorder level: %{x}<extra></extra>"))
    fig2.update_layout(yaxis={"categoryorder": "array", "categoryarray": low["product"].tolist()}, xaxis_title="Units", barmode="overlay")

    category_value = df.groupby("category").stock_value_demo.sum().sort_values(ascending=True)
    fig3 = styled(go.Figure())
    fig3.add_trace(go.Bar(x=category_value.values, y=category_value.index, orientation="h", marker_color=BLUE, hovertemplate="%{y}<br>Demo stock value: %{x:.2f}<extra></extra>"))
    fig3.update_layout(xaxis_title="Illustrative value units", showlegend=False)

    expiry = df.sort_values("days_to_expiry_demo").head(18)
    fig4 = styled(go.Figure(), 390)
    fig4.add_trace(go.Bar(x=expiry.days_to_expiry_demo, y=expiry["product"], orientation="h", marker_color=[CORAL if x <= 60 else GOLD if x <= 120 else TEAL for x in expiry.days_to_expiry_demo], hovertemplate="%{y}<br>Days to demo expiry: %{x}<extra></extra>"))
    fig4.add_vline(x=60, line_dash="dash", line_color=CORAL, annotation_text="60-day review guide")
    fig4.update_layout(yaxis={"categoryorder": "array", "categoryarray": expiry["product"].tolist()}, xaxis_title="Days remaining (synthetic)", showlegend=False)

    inventory_value = float(df.stock_value_demo.sum())
    urgent_count = int((df.status_demo == "Urgent reorder").sum())
    reorder_count = int((df.status_demo == "Reorder").sum())
    expiry_count = int((df.days_to_expiry_demo <= 60).sum())
    metrics = [
        ("Demo SKUs", str(len(df)), "Generated product list"),
        ("Urgent", str(urgent_count), "Below 45% of reorder level"),
        ("Reorder", str(reorder_count), "Below configured threshold"),
        ("Expiry watch", str(expiry_count), "Within 60 synthetic days"),
    ]
    write_dashboard(
        slug,
        "Pharmacy Inventory & Alert System",
        "A lightweight stock-monitoring prototype that highlights reorder thresholds, inventory mix and upcoming expiry dates.",
        metrics,
        [("Stock status overview", fig1), ("Lowest stock versus reorder level", fig2), ("Illustrative value by category", fig3), ("Expiry review queue", fig4)],
        [
            f"The sample inventory has an illustrative total stock value of {inventory_value:,.2f} units.",
            "Urgent and reorder flags are computed from the example quantities and thresholds in the CSV.",
            "A real deployment should use verified inventory, approved policies and staff review before acting on alerts.",
        ],
        "sample_inventory.csv",
        "sample_alerts.csv",
        "Prototype only: all products, quantities, costs and dates are synthetic. This is not medical, purchasing or expiry-management advice.",
    )
    write_readme(slug, "Pharmacy Inventory & Alert System", "A generated Python prototype for the portfolio's spreadsheet / n8n inventory-alert concept.", "simulate.py", "- `data/sample_inventory.csv` — synthetic stock, reorder and expiry fields.\n- `data/sample_alerts.csv` — generated review queue.\n- `dashboard.html` — interactive stock and expiry views.", "All inventory values are synthetic. The demo does not recommend purchases or replace the pharmacy's approved inventory and expiry procedures.")


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


def pill(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], label: str, fill: str, text_color: str = "#FFFFFF") -> None:
    draw.rounded_rectangle(box, radius=18, fill=fill)
    draw.text((box[0] + 14, box[1] + 8), label, font=font(18, True), fill=text_color)


def create_cover(slug: str, index: str, title: str, subtitle: str, motif: str, accent: str) -> None:
    width, height = 1600, 900
    img = Image.new("RGB", (width, height))
    px = img.load()
    c0 = (23, 39, 52)
    c1 = (37, 83, 91)
    for y in range(height):
        t = y / (height - 1)
        c = tuple(round(c0[i] * (1 - t) + c1[i] * t) for i in range(3))
        for x in range(width):
            glow = max(0, 1 - abs(x - 1320) / 680) * 0.18
            px[x, y] = tuple(round(channel * (1 - glow) + (45, 110, 112)[i] * glow) for i, channel in enumerate(c))
    d = ImageDraw.Draw(img, "RGBA")
    for x in range(0, width, 48):
        d.line((x, 0, x, height), fill=(255, 255, 255, 14), width=1)
    for y in range(0, height, 48):
        d.line((0, y, width, y), fill=(255, 255, 255, 14), width=1)
    d.ellipse((970, -330, 1780, 480), fill=(255, 255, 255, 12))
    d.ellipse((1140, 560, 1760, 1180), fill=(230, 107, 93, 18))

    d.text((82, 82), f"PROJECT {index}  /  GIFT SIFWAKU", font=font(21, True), fill="#B6D1D4")
    d.rounded_rectangle((82, 132, 160, 139), radius=3, fill=accent)
    wrapped = ["Pharmacy", "Inventory &", "Alert System"] if motif == "pharmacy" else textwrap.wrap(title, width=21)
    title_size = 56 if motif == "pharmacy" else 62
    y = 190
    for line in wrapped[:3]:
        d.text((80, y), line, font=font(title_size, True), fill="#FFFFFF", stroke_width=0)
        y += 70 if motif == "pharmacy" else 76
    d.text((84, y + 24), subtitle, font=font(25), fill="#DCE8E9")
    pill(d, (84, 755, 295, 804), "PYTHON DEMO", accent)
    d.text((84, 828), "SYNTHETIC SAMPLE DATA  •  PORTFOLIO PROJECT", font=font(16, True), fill="#C1D6D8")

    # Main visual stage
    stage = (755, 130, 1518, 755)
    d.rounded_rectangle((stage[0] + 12, stage[1] + 15, stage[2] + 12, stage[3] + 15), radius=34, fill=(0, 0, 0, 48))
    d.rounded_rectangle(stage, radius=32, fill=(248, 250, 250, 255))
    d.text((805, 170), "PROJECT SNAPSHOT", font=font(18, True), fill=NAVY)
    d.line((805, 214, 1468, 214), fill=LINE, width=2)

    if motif == "student":
        d.text((810, 250), "LEARNING INSIGHTS", font=font(26, True), fill=NAVY)
        d.text((810, 291), "Score patterns  /  sample cohort", font=font(17), fill="#60717D")
        d.rounded_rectangle((812, 347, 1456, 659), radius=18, fill="#F1F5F6")
        for j in range(5):
            gy = 390 + j * 48
            d.line((852, gy, 1415, gy), fill=(205, 216, 220), width=2)
        heights = [55, 91, 76, 132, 115, 167, 146, 210]
        for j, value in enumerate(heights):
            x = 875 + j * 62
            color = accent if j in (4, 7) else (39, 138, 131)
            d.rounded_rectangle((x, 625 - value, x + 34, 626), radius=9, fill=color)
        line_points = [(880 + j * 62, 545 - heights[j] * 0.55) for j in range(8)]
        d.line(line_points, fill=CORAL, width=5, joint="curve")
        for x, y0 in line_points:
            d.ellipse((x - 7, y0 - 7, x + 7, y0 + 7), fill=CORAL, outline="white", width=3)
        pill(d, (812, 685, 1015, 728), "STUDY HOURS", NAVY)
        pill(d, (1030, 685, 1226, 728), "SCORE TRENDS", TEAL)
    elif motif == "basket":
        d.text((810, 250), "PRODUCT CONNECTIONS", font=font(26, True), fill=NAVY)
        d.text((810, 291), "Association patterns  /  generated baskets", font=font(17), fill="#60717D")
        nodes = [(930, 405, "COFFEE", CORAL), (1260, 405, "BREAD", TEAL), (1055, 570, "MILK", BLUE), (1370, 585, "SUGAR", GOLD)]
        for a, b in ((0, 1), (0, 2), (1, 2), (1, 3), (2, 3)):
            d.line((nodes[a][0], nodes[a][1], nodes[b][0], nodes[b][1]), fill=(39, 78, 92, 90), width=5)
        for x, y0, label, color in nodes:
            d.ellipse((x - 62, y0 - 62, x + 62, y0 + 62), fill=color)
            # compact shopping-bag mark
            d.rounded_rectangle((x - 25, y0 - 18, x + 25, y0 + 34), radius=7, fill="#FFFFFF")
            d.arc((x - 15, y0 - 34, x + 15, y0 + 8), 180, 360, fill="#FFFFFF", width=5)
            d.text((x - 52, y0 + 76), label, font=font(16, True), fill=NAVY)
        pill(d, (814, 685, 1030, 728), "SUPPORT", NAVY)
        pill(d, (1045, 685, 1284, 728), "CONFIDENCE + LIFT", TEAL)
    elif motif == "bird":
        d.text((810, 250), "FIELD TELEMETRY", font=font(26, True), fill=NAVY)
        d.text((810, 291), "Route + tag health  /  simulated GPS fixes", font=font(17), fill="#60717D")
        map_box = (812, 347, 1456, 659)
        d.rounded_rectangle(map_box, radius=18, fill="#EAF2F0")
        for j in range(7):
            xx = 850 + j * 88
            d.line((xx, 370, xx + 40, 635), fill=(197, 216, 211), width=2)
        route = [(865, 590), (965, 540), (1055, 550), (1120, 478), (1230, 465), (1300, 402), (1410, 385)]
        d.line(route, fill=accent, width=8, joint="curve")
        for j, (x, y0) in enumerate(route):
            r = 11 if j in (0, len(route) - 1) else 7
            d.ellipse((x - r, y0 - r, x + r, y0 + r), fill=accent if j == len(route) - 1 else TEAL, outline="white", width=3)
        # simplified bird silhouette in flight
        bx, by = 1190, 500
        d.polygon([(bx - 70, by), (bx - 10, by - 34), (bx + 4, by - 4), (bx + 24, by - 31), (bx + 82, by - 4), (bx + 32, by - 12), (bx + 7, by + 13), (bx - 7, by - 2)], fill=NAVY)
        pill(d, (812, 685, 1025, 728), "GPS FIXES", NAVY)
        pill(d, (1040, 685, 1277, 728), "BATTERY + SIGNAL", TEAL)
    else:
        d.text((810, 250), "INVENTORY CONTROL", font=font(26, True), fill=NAVY)
        d.text((810, 291), "Stock + expiry watch  /  simulated inventory", font=font(17), fill="#60717D")
        # Shelf and product cartons
        d.rounded_rectangle((812, 350, 1112, 654), radius=18, fill="#EEF3F4")
        for shelf_y in (435, 530, 625):
            d.rounded_rectangle((835, shelf_y, 1087, shelf_y + 12), radius=5, fill="#526A78")
        box_colors = [CORAL, TEAL, BLUE, GOLD, "#7A6CA8", "#86A96F", "#D78363", "#5394A2"]
        k = 0
        for shelf_top in (365, 460, 555):
            for j in range(4):
                x = 840 + j * 61
                h = 52 + (j % 2) * 13
                d.rounded_rectangle((x, shelf_top + 10, x + 46, shelf_top + 10 + h), radius=5, fill=box_colors[k % len(box_colors)])
                d.rectangle((x + 8, shelf_top + 24, x + 37, shelf_top + 30), fill=(255, 255, 255, 190))
                k += 1
        # Alert panel
        d.rounded_rectangle((1145, 350, 1457, 654), radius=20, fill="#F5F7F8", outline=LINE, width=2)
        d.ellipse((1180, 382, 1234, 436), fill=(230, 107, 93, 32), outline=CORAL, width=3)
        d.text((1195, 388), "!", font=font(38, True), fill=CORAL)
        d.text((1252, 388), "STOCK ALERT", font=font(18, True), fill=NAVY)
        for j, (label, value, color) in enumerate((("Urgent", 0.72, CORAL), ("Reorder", 0.48, GOLD), ("In stock", 0.86, TEAL))):
            yy = 470 + j * 55
            d.text((1180, yy), label, font=font(16, True), fill="#536575")
            d.rounded_rectangle((1275, yy + 2, 1415, yy + 17), radius=8, fill="#DCE5E8")
            d.rounded_rectangle((1275, yy + 2, int(1275 + 140 * value), yy + 17), radius=8, fill=color)
        pill(d, (1148, 685, 1342, 728), "REORDER WATCH", accent)

    img.save(COVERS / f"{slug}.jpg", quality=91, optimize=True)


def generate_covers() -> None:
    COVERS.mkdir(parents=True, exist_ok=True)
    create_cover("student-performance-analysis", "01", "Student Performance Analysis", "A clearer view of learning patterns", "student", CORAL)
    create_cover("market-basket-analysis", "02", "Market Basket Analysis", "Discover useful product relationships", "basket", TEAL)
    create_cover("bird-migration-tracking", "03", "Bird Migration Tracking System", "A connected view of sample telemetry", "bird", BLUE)
    create_cover("pharmacy-inventory-alert", "04", "Pharmacy Inventory & Alert System", "Stock signals, organized for review", "pharmacy", GOLD)


def main() -> None:
    PROJECTS.mkdir(exist_ok=True)
    generate_student_performance()
    generate_market_basket()
    generate_bird_tracking()
    generate_pharmacy_inventory()
    generate_covers()
    print("Built four Python project demos, interactive dashboards, sample datasets, and original cover illustrations.")
    for slug in (
        "student-performance-analysis",
        "market-basket-analysis",
        "bird-migration-tracking",
        "pharmacy-inventory-alert",
    ):
        print(f"  projects/{slug}/dashboard.html")
    print("  assets/projects/*.jpg")


if __name__ == "__main__":
    main()
