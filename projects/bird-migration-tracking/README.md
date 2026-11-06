# Bird Migration Tracking System

A simulated Python telemetry dashboard supporting the portfolio's ESP32 / LoRa / Wi-Fi system concept.

## Run the demo

From the portfolio repository root:

```bash
python -m pip install -r projects/requirements.txt
python projects/build_portfolio_demos.py
```

The script writes its synthetic input data and analysis outputs into this project folder. Open `dashboard.html` in a browser to explore the charts.

## Files

- `data/sample_telemetry.csv` — generated GPS and tag-health readings.
- `dashboard.html` — route and device-health visualizations.

## Data note

Coordinates and sensor values are synthetic. This demo is not wildlife research and does not claim a real migration route.
