# crypto-risk-simulator
Crypto Derivatives and Risk Simulator Demo is a Python‑based toolkit for simulating order execution, pricing forwards, and measuring portfolio risk in cryptocurrency markets. The demo shows how risk metrics and execution quality can be integrated into a single workflow. It uses synthetic or snapshot data for reproducibility, but can be extended to pull live market feeds via CCXT or exchange APIs.

It demonstrates how to:
= Capture market snapshots (spot order books, mid‑price, spreads)
= Simulate execution strategies such as VWAP (Volume Weighted Average Price) and TWAP (Time Weighted Average Price)
= Track PnL and fees for executed trades
= Compute Value‑at‑Risk (VaR) using both long‑horizon (250 days) and short‑horizon (60 days) lookbacks, plus intraday hourly risk
= Run stress scenarios to see portfolio impact under shocks
= Summarize results in a clean, tabulated log output

## Features
- Capture spot order book snapshots
- Simulate VWAP and TWAP execution
- Track PnL and fees
- Compute VaR (250‑day, 60‑day, and intraday horizons)
- Run stress scenarios under price shocks
- Summarize results in a clean tabulated log

# Installation
Clone the repository and install dependencies:

git clone https://github.com/528Insights/crypto-risk-simulator.git
cd crypto-risk-simulator
pip install -r requirements.txt

Project Structure
crypto-risk-simulator/
├─ README.md
├─ requirements.txt
├─ config.py
├─ data/
│  └─ samples/                # saved snapshots for reproducible runs
├─ core/
│  ├─ exchange_client.py      # unified exchange access (spot + perp)
│  ├─ market_data.py          # streaming/polling, snapshots
│  ├─ ndf_pricer.py           # forward curve + spreads
│  ├─ execution.py            # VWAP/TWAP block trade simulator
│  ├─ risk.py                 # PnL, VaR, stress tests, inventory
│  └─ microprice_simulator.py # price simulator

├─ app/
│  └─ crypto_dashboard.py     # optional Streamlit dashboard
└─ demo.py                    # quick end-to-end demo

Notes
Demo prices may use synthetic snapshots for reproducibility.
Switch to live mode with CCXT/exchange APIs to reflect current BTC prices.
For educational and research purposes only.


