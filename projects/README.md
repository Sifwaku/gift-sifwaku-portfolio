# Python Project Demos

Four small, reproducible Python demonstrations accompany the projects on Gift Sifwaku's portfolio. Each has an interactive HTML dashboard, downloadable CSV data and project notes.

## Build or refresh all demos

From the repository root:

```bash
python -m pip install -r projects/requirements.txt
python projects/build_portfolio_demos.py
```

The builder also creates the coordinated project cover illustrations in `assets/projects/`.

## Projects

- `student-performance-analysis/` — exploratory analysis of study time, attendance, assignments and synthetic scores.
- `market-basket-analysis/` — item-set support, association-rule confidence and lift for generated baskets.
- `bird-migration-tracking/` — simulated GPS and tag-health telemetry for the connected-systems concept.
- `pharmacy-inventory-alert/` — synthetic stock thresholds, reorder flags and expiry-review example.

## Data note

All records are generated examples. They do not represent actual students, customers, wildlife or pharmacy stock. The simulated dashboards are portfolio demonstrations and should be replaced with approved project data if used in real work.
