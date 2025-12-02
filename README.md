# crypto-risk-simulator
Crypto Derivatives and Risk Simulator Demo is a Python‑based toolkit for simulating order execution, pricing forwards, and measuring portfolio risk in cryptocurrency markets. The demo shows how risk metrics and execution quality can be integrated into a single workflow. It uses synthetic or snapshot data for reproducibility, but can be extended to pull live market feeds via CCXT or exchange APIs.

It demonstrates how to:
= Capture market snapshots (spot order books, mid‑price, spreads)
= Simulate execution strategies such as VWAP (Volume Weighted Average Price) and TWAP (Time Weighted Average Price)
= Track PnL and fees for executed trades
= Compute Value‑at‑Risk (VaR) using both long‑horizon (250 days) and short‑horizon (60 days) lookbacks, plus intraday hourly risk
= Run stress scenarios to see portfolio impact under shocks
= Summarize results in a clean, tabulated log output

## 🚀 Features
- Capture spot order book snapshots
- Simulate VWAP and TWAP execution
- Track PnL and fees
- Compute VaR (250‑day, 60‑day, and intraday horizons)
- Run stress scenarios under price shocks
- Summarize results in a clean tabulated log

## Installation
Clone the repository and install dependencies:

git clone https://github.com/528Insights/crypto-risk-simulator.git
cd crypto-risk-simulator
pip install -r requirements.txt

USAGE
python demo.py

Project Structure
crypto-risk-simulator/
├── demo.py              # Main demo script
├── requirements.txt     # Python dependencies
├── data/samples/        # Saved snapshots and results
└── README.md            # Project documentation

Notes
Demo prices may use synthetic snapshots for reproducibility.
Switch to live mode with CCXT/exchange APIs to reflect current BTC prices.
For educational and research purposes only.


SAMPLE Output
2025-12-02 09:40:53,557 [INFO] === Starting Crypto Derivatives and Risk Simulator Demo at 2025-12-02 09:40:53 UTC ===
2025-12-02 09:40:53,558 [INFO] Running in snapshot mode: capturing a single spot order book
2025-12-02 09:40:59,373 [INFO] Saved single snapshot to data/samples/orderbook_snapshot.csv
2025-12-02 09:40:59,375 [INFO] Mid price: 86661.36, top spread: 0.01
2025-12-02 09:40:59,378 [INFO] NDF 7D Forward: 86711.24 | Bid: 86602.85 | Ask: 86819.63
2025-12-02 09:40:59,378 [INFO] VWAP avg: 86895.66, slippage: -0.0 bps
2025-12-02 09:40:59,378 [INFO] TWAP avg: 86903.05, slippage: 0.0 bps
2025-12-02 09:40:59,378 [INFO] Unrealized PnL: 4475.09, Fees estimate: 100.27, Net: 4374.82
2025-12-02 09:40:59,378 [INFO] ---- Risk Analysis ----
2025-12-02 09:40:59,858 [INFO] Resampled Historical 99% Long VaR (250 days) on $500,000: $45,350
2025-12-02 09:40:59,858 [INFO] Resampled Historical 99% Short VaR (60 days) on $500,000: $45,350
2025-12-02 09:40:59,876 [INFO] Hourly Intraday 99% VaR on $500,000: $28,137
2025-12-02 09:40:59,877 [INFO]
|    |   Shock |   Fees |   Volatility |   Shocked Price |   Net PnL |
|----|---------|--------|--------------|-----------------|-----------|
|  0 |    -0.2 |    1   |          1   |         69329.1 | -100600   |
|  1 |    -0.2 |    1   |          1.5 |         69329.1 | -100700   |
|  2 |    -0.2 |    1   |          2   |         69329.1 | -100800   |
|  3 |    -0.2 |    1.5 |          1   |         69329.1 | -100800   |
|  4 |    -0.2 |    1.5 |          1.5 |         69329.1 | -100900   |
|  5 |    -0.2 |    1.5 |          2   |         69329.1 | -101000   |
|  6 |    -0.2 |    2   |          1   |         69329.1 | -101000   |
|  7 |    -0.2 |    2   |          1.5 |         69329.1 | -101100   |
|  8 |    -0.2 |    2   |          2   |         69329.1 | -101200   |
|  9 |    -0.1 |    1   |          1   |         77995.2 |  -50675   |
| 10 |    -0.1 |    1   |          1.5 |         77995.2 |  -50787.5 |
| 11 |    -0.1 |    1   |          2   |         77995.2 |  -50900   |
| 12 |    -0.1 |    1.5 |          1   |         77995.2 |  -50900   |
| 13 |    -0.1 |    1.5 |          1.5 |         77995.2 |  -51012.5 |
| 14 |    -0.1 |    1.5 |          2   |         77995.2 |  -51125   |
| 15 |    -0.1 |    2   |          1   |         77995.2 |  -51125   |
| 16 |    -0.1 |    2   |          1.5 |         77995.2 |  -51237.5 |
| 17 |    -0.1 |    2   |          2   |         77995.2 |  -51350   |
| 18 |     0.1 |    1   |          1   |         95327.5 |   49175   |
| 19 |     0.1 |    1   |          1.5 |         95327.5 |   49037.5 |
| 20 |     0.1 |    1   |          2   |         95327.5 |   48900   |
| 21 |     0.1 |    1.5 |          1   |         95327.5 |   48900   |
| 22 |     0.1 |    1.5 |          1.5 |         95327.5 |   48762.5 |
| 23 |     0.1 |    1.5 |          2   |         95327.5 |   48625   |
| 24 |     0.1 |    2   |          1   |         95327.5 |   48625   |
| 25 |     0.1 |    2   |          1.5 |         95327.5 |   48487.5 |
| 26 |     0.1 |    2   |          2   |         95327.5 |   48350   |
| 27 |     0.2 |    1   |          1   |        103994   |   99100   |
| 28 |     0.2 |    1   |          1.5 |        103994   |   98950   |
| 29 |     0.2 |    1   |          2   |        103994   |   98800   |
| 30 |     0.2 |    1.5 |          1   |        103994   |   98800   |
| 31 |     0.2 |    1.5 |          1.5 |        103994   |   98650   |
| 32 |     0.2 |    1.5 |          2   |        103994   |   98500   |
| 33 |     0.2 |    2   |          1   |        103994   |   98500   |
| 34 |     0.2 |    2   |          1.5 |        103994   |   98350   |
| 35 |     0.2 |    2   |          2   |        103994   |   98200   |

| Metric              | Value    |
|---------------------|----------|
| Mid Price           | 86661.36 |
| NDF Forward (1W)    | 86711.24 |
| NDF Bid             | 86602.85 |
| NDF Ask             | 86819.63 |
| VWAP Avg            | 86895.66 |
| VWAP Slippage (bps) | -0.0     |
| TWAP Avg            | 86903.05 |
| TWAP Slippage (bps) | 0.0      |
| Unrealized PnL      | 4475.09  |
| Fees Estimate       | 100.27   |
| Net PnL             | 4374.82  |
| VaR 99% Long        | 45,350   |
| VaR 99% Short       | 45,350   |
2025-12-02 09:41:00,312 [INFO]  Demo finished in snapshot mode. Results saved to data/samples/orderbook_snapshot.csv
2025-12-02 09:41:00,312 [INFO] === Demo Completed Successfully at 2025-12-02 09:41:00 UTC===
2025-12-02 09:41:00,312 [INFO] Total runtime: 0 days 00:00:06

