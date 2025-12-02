import math
import numpy as np
import pandas as pd
from dataclasses import dataclass


@dataclass
class NDFQuote:
    forward: float
    bid: float
    ask: float

def crypto_forward_curve(spot: float,
                         funding_dom: float,
                         funding_crypto: float,
                         tenors_days: list,
                         spread_bp: float = 20) -> pd.DataFrame:
    """
    Compute crypto forward quotes for multiple tenors.

    spot          : spot price of the crypto (e.g., BTC/USD)
    funding_dom   : domestic funding/lending rate (USD) annualized
    funding_crypto: crypto funding rate (BTC, ETH, etc.) annualized
    tenors_days   : list of maturities in days
    spread_bp     : bid/ask spread in basis points
    """
    T = np.array(tenors_days) / 365.0
    forwards = spot * np.exp((funding_dom - funding_crypto) * T)
    half_spread = forwards * spread_bp / 10000 / 2
    bids = forwards - half_spread
    asks = forwards + half_spread

    df = pd.DataFrame({
        'tenor_days': tenors_days,
        'forward': forwards,
        'bid': bids,
        'ask': asks
    })
    return df

def make_ndf_quote(spot: float, r_annual: float, q_annual: float,
                   tenor_days: int = 7, spread_bp: int = 25) -> NDFQuote:
    """
    Return a single NDF quote for one tenor.
    spot       : current spot or perp mid price
    r_annual   : domestic interest rate (annualized)
    q_annual   : crypto funding rate (annualized)
    tenor_days : tenor in days
    spread_bp  : dealer spread in basis points
    """
    df = crypto_forward_curve(spot, r_annual, q_annual, [tenor_days], spread_bp)
    row = df.iloc[0]
    return NDFQuote(forward=row['forward'], bid=row['bid'], ask=row['ask'])

# Example usage
spot = 500000
funding_dom = 0.05
funding_crypto = -0.02
tenors = [1, 7, 30, 90, 180]

curve = crypto_forward_curve(spot, funding_dom, funding_crypto, tenors)
print(curve)
