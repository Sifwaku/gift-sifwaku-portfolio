# Python Project Demos

Four reproducible Python demonstrations and an HR visualization project accompany the projects on Gift Sifwaku's portfolio. Each has an interactive HTML dashboard, downloadable CSV data and project notes.

## Build or refresh all demos

From the repository root:

```bash
python -m pip install -r projects/requirements.txt
python projects/build_portfolio_demos.py
python projects/build_hr_visualization.py
```

The first builder refreshes the four generated demo projects and creates only missing cover illustrations, preserving existing project snapshots. The HR builder uses the included Kaggle CSV and updates only the HR dashboard, its analysis summaries and its portfolio snapshot.

## Projects

- `student-performance-analysis/` — exploratory analysis of study time, attendance, assignments and synthetic scores.
- `hr-attrition-visualization/` — interactive visual exploration of a fictional IBM HR attrition dataset hosted on Kaggle.
- `market-basket-analysis/` — item-set support, association-rule confidence and lift for generated baskets.
- `bird-migration-tracking/` — simulated GPS and tag-health telemetry for the connected-systems concept.
- `pharmacy-inventory-alert/` — synthetic stock thresholds, reorder flags and expiry-review example.

## Data note

The student, shopping, wildlife and pharmacy demo records are generated examples. The HR visualization uses IBM's fictional HR analytics dataset from Kaggle; source and license attribution are included in that project. None of these dashboards represent current real-world operations, and their observed relationships should not be treated as causal.
