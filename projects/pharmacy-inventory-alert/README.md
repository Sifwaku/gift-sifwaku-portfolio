# Pharmacy Inventory & Alert System

A generated Python prototype for the portfolio's spreadsheet / n8n inventory-alert concept.

## Run the demo

From the portfolio repository root:

```bash
python -m pip install -r projects/requirements.txt
python projects/build_portfolio_demos.py
```

The script writes its synthetic input data and analysis outputs into this project folder. Open `dashboard.html` in a browser to explore the charts.

## Files

- `data/sample_inventory.csv` — synthetic stock, reorder and expiry fields.
- `data/sample_alerts.csv` — generated review queue.
- `dashboard.html` — interactive stock and expiry views.

## Data note

All inventory values are synthetic. The demo does not recommend purchases or replace the pharmacy's approved inventory and expiry procedures.
