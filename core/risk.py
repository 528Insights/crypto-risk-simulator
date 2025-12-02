import numpy as np
import pandas as pd
from dataclasses import dataclass

@dataclass
class PnLReport:
    realized: float
    unrealized: float
    total: float
    inventory: float

def inventory_pnl(trade_prices, trade_qtys, current_price) -> PnLReport:
    # simple average cost inventory
    qty = np.sum(trade_qtys)
    cost = np.sum(trade_prices * trade_qtys) / max(qty, 1e-9)
    unreal = (current_price - cost) * qty
    realized = 0.0  # extend if you close trades
    return PnLReport(realized=realized, unrealized=float(unreal), total=float(unreal), inventory=float(qty))

def historical_var(returns: pd.Series, alpha: float = 0.99, notional: float = 100000.0) -> float:
    # historical simulation VaR: positive number as loss
    r_sorted = returns.dropna().sort_values()
    idx = int((1 - alpha) * len(r_sorted))
    var_pct = r_sorted.iloc[idx]  # negative
    return abs(var_pct) * notional

def stress_scenarios(
    current_price: float,
    shocks_pct = (-0.2, -0.1, +0.1, +0.2),
    position_qty: float = 1.0,
    base_fee_bp: float = 10.0,
    fee_multipliers = (1.0, 1.5, 2.0),
    vol_multipliers = (1.0, 1.5, 2.0),
    slippage_bp: float = 5.0
):
    """
    Run stress scenarios by shocking price, fees, and volatility.

    - Price shocks: apply percentage changes to the current price.
    - Fee multipliers: scale trading fees to simulate liquidity stress.
    - Volatility multipliers: scale slippage costs to simulate execution risk under higher volatility.

    Net PnL is computed as:
        (PnL from price shock) - (fees) - (slippage cost scaled by volatility multiplier)

    Returns:
        pd.DataFrame with columns:
            Shock (price shock %),
            Fees (fee multiplier),
            Volatility (vol multiplier),
            Shocked Price (new price after shock),
            Net PnL (profit/loss after fees and slippage).
    """    
    rows = []
    for s in shocks_pct:
        shocked_price = current_price * (1 + s)
        pnl = (shocked_price - current_price) * position_qty

        for fm in fee_multipliers:
            fees = (base_fee_bp / 10000.0) * shocked_price * position_qty * fm
            for vm in vol_multipliers:
                # Slippage grows with volatility multiplier
                slippage_cost = (slippage_bp / 10000.0) * shocked_price * position_qty * vm
                net_pnl = pnl - fees - slippage_cost
                rows.append({
                    "Shock": s,
                    "Fees": fm,
                    "Volatility": vm,
                    "Shocked Price": shocked_price,
                    "Net PnL": net_pnl
                })
    return pd.DataFrame(rows)

# def stress_scenarios(
#     current_price: float,
#     shocks_pct = (-0.2, -0.1, +0.1, +0.2),
#     position_qty: float = 1.0,
#     base_fee_bp: float = 10.0,
#     fee_multipliers = (1.0, 1.5, 2.0),
#     vol_multipliers = (1.0, 1.5, 2.0)
# ):
#   """ Run stress scenarios by shocking price, fees, and volatility. Returns a DataFrame with all combinations. """
#     rows = []
#     for s in shocks_pct:
#         shocked_price = current_price * (1 + s)
#         pnl = (shocked_price - current_price) * position_qty

#         for fm in fee_multipliers:
#             fees = (base_fee_bp / 10000.0) * shocked_price * position_qty * fm
#             for vm in vol_multipliers:
#                 net_pnl = pnl - fees
#                 rows.append({
#                     "shock_pct": s,
#                     "fee_mult": fm,
#                     "vol_mult": vm,
#                     "shocked_price": shocked_price,
#                     "net_pnl": net_pnl
#                 })

#     return pd.DataFrame(rows)

# def stress_scenarios(current_price: float, shocks_pct = (-0.2, -0.1, +0.1, +0.2), position_qty: float = 1.0):
#     rows = []
#     for s in shocks_pct:
#         shocked = current_price * (1 + s)
#         pnl = (shocked - current_price) * position_qty
#         rows.append({'shock_pct': s, 'shocked_price': shocked, 'pnl': pnl})
#     return pd.DataFrame(rows)
