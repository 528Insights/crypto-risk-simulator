import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass

# --- Execution dataclass ---
@dataclass
class ExecutionResult:
    algorithm: str
    avg_price: float
    slippage_bps: float
    schedule: pd.DataFrame

# --- VWAP executor ---
def vwap_execute(prices: np.ndarray, volumes: np.ndarray, target_qty: float) -> ExecutionResult:
    weights = volumes / volumes.sum()
    schedule_qty = target_qty * weights
    avg_price = (prices * schedule_qty).sum() / schedule_qty.sum()
    bench = (prices * volumes).sum() / volumes.sum()
    slippage_bps = (avg_price - bench) / bench * 10000
    schedule = pd.DataFrame({'price': prices, 'volume': volumes, 'qty_exec': schedule_qty})
    return ExecutionResult('VWAP', float(avg_price), float(slippage_bps), schedule)

# --- TWAP executor ---
def twap_execute(prices: np.ndarray, target_qty: float) -> ExecutionResult:
    n = len(prices)
    schedule_qty = np.full(n, target_qty / n)
    avg_price = (prices * schedule_qty).sum() / target_qty
    bench = prices.mean()
    slippage_bps = (avg_price - bench) / bench * 10000
    schedule = pd.DataFrame({'price': prices, 'qty_exec': schedule_qty})
    return ExecutionResult('TWAP', float(avg_price), float(slippage_bps), schedule)

# --- Simulated BTCUSD order book ---
np.random.seed(42)
prices = np.array([30000, 30100, 29950, 30050, 30200, 30150, 30080, 30120, 30060, 30100])
volumes = np.array([2.5, 3.0, 1.8, 2.2, 2.9, 3.1, 2.0, 2.5, 1.9, 2.3])  # BTC traded per slice
target_qty = 10  # BTC to buy

# --- Run VWAP and TWAP ---
vwap_res = vwap_execute(prices, volumes, target_qty)
twap_res = twap_execute(prices, target_qty)

# --- Display results ---
print(f"VWAP Execution: Avg Price={vwap_res.avg_price:.2f}, Slippage={vwap_res.slippage_bps:.2f} bps")
print(vwap_res.schedule, "\n")

print(f"TWAP Execution: Avg Price={twap_res.avg_price:.2f}, Slippage={twap_res.slippage_bps:.2f} bps")
print(twap_res.schedule, "\n")

# --- Plot execution schedules ---
plt.figure(figsize=(12,6))
plt.plot(vwap_res.schedule['qty_exec'].cumsum(), vwap_res.schedule['price'], marker='o', label='VWAP')
plt.plot(twap_res.schedule['qty_exec'].cumsum(), twap_res.schedule['price'], marker='x', label='TWAP')
plt.xlabel('Cumulative BTC Executed')
plt.ylabel('Price (USD)')
plt.title('VWAP vs TWAP Execution Schedule')
plt.legend()
plt.grid(True)
plt.show()
