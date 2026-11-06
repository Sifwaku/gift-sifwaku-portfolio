# Market Basket Analysis

A small, transparent Apriori-style association-rule demo using Python, pandas, NumPy and Plotly.

## Run the demo

From the portfolio repository root:

```bash
python -m pip install -r projects/requirements.txt
python projects/build_portfolio_demos.py
```

The script writes its synthetic input data and analysis outputs into this project folder. Open `dashboard.html` in a browser to explore the charts.

## Files

- `data/sample_basket_items.csv` — generated transaction-item rows.
- `data/association_rules.csv` — mined rules with support, confidence and lift.
- `dashboard.html` — interactive report.

## Data note

Every basket is synthetic and generated with known example patterns so the calculations can be explored. The results are not real retail findings.
