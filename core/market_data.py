import time
import pandas as pd
import ccxt

# Initialise clients
spot = ccxt.binance()
futures = ccxt.binance({'options': {'defaultType': 'future'}})

# Utility functions
def mid_from_order_book(bids, asks) -> float:
    if not bids or not asks:
        return float('nan')
    return (bids[0][0] + asks[0][0]) / 2.0

def spread_top(bids, asks) -> float:
    if not bids or not asks:
        return float('nan')
    return asks[0][0] - bids[0][0]

def depth_snapshot(bids, asks, depth: int = 20) -> pd.DataFrame:
    """
    Create a snapshot DataFrame of order book depth.
    Returns a DataFrame with columns: price, size, side
    """
    bid_df = pd.DataFrame(bids[:depth], columns=['price', 'size'])
    bid_df['side'] = 'bid'
    ask_df = pd.DataFrame(asks[:depth], columns=['price', 'size'])
    ask_df['side'] = 'ask'
    return pd.concat([bid_df, ask_df], ignore_index=True)

# --- Single-market polling(spot) ---
def poll_order_book(client, symbol: str,
                    limit: int = 50, n: int = 10, sleep_s: float = 1.0) -> pd.DataFrame:
    """
    Poll a single market's order book n times and compute mid and spread.
    Returns a DataFrame with timestamp, mid, spread.
    """
    #Updated to fix NaT values
    rows = []
    for _ in range(n):
        ob = client.fetch_order_book(symbol, limit=limit)
        ts_raw = ob.get('timestamp')
        ts = pd.to_datetime(ts_raw, unit='ms') if ts_raw else pd.Timestamp.utcnow()
        rows.append({
            'timestamp': ts,
            'mid': mid_from_order_book(ob['bids'], ob['asks']),
            'spread': spread_top(ob['bids'], ob['asks'])
        })
        time.sleep(sleep_s)
    return pd.DataFrame(rows)

# returned NaT when ran
# def poll_order_book(client, symbol: str,
#                     limit: int = 50, n: int = 10, sleep_s: float = 1.0) -> pd.DataFrame:
#     """
#     Poll a single market's order book n times and compute mid and spread.
#     Returns a DataFrame with timestamp, mid, spread.    
#     # rows = []
    # for _ in range(n):
    #     ob = client.fetch_order_book(symbol, limit=limit)
    #     mid = mid_from_order_book(ob['bids'], ob['asks'])
    #     spr = spread_top(ob['bids'], ob['asks'])
    #     rows.append({
    #         'timestamp': pd.to_datetime(ob['timestamp'], unit='ms'),
    #         'mid': mid,
    #         'spread': spr
    #     })
    #     time.sleep(sleep_s)
    # return pd.DataFrame(rows)

# --- Dual-market polling (spot + perp) ---
def poll_order_books(spot_client, futures_client, symbol: str,
                     limit: int = 50, n: int = 10, sleep_s: float = 1.0) -> pd.DataFrame:
    """
    Poll both Spot and Futures order books n times and compute mid and spread at each snapshot.
    Returns a combined DataFrame with market labels and valid timestamps.
    """
    rows = []
    for _ in range(n):
        # Spot
        ob_spot = spot_client.fetch_order_book(symbol, limit=limit)
        ts_spot_raw = ob_spot.get('timestamp')
        ts_spot = pd.to_datetime(ts_spot_raw, unit='ms') if ts_spot_raw else pd.Timestamp.utcnow()
        rows.append({
            'timestamp': ts_spot,
            'market': 'spot',
            'mid': mid_from_order_book(ob_spot['bids'], ob_spot['asks']),
            'spread': spread_top(ob_spot['bids'], ob_spot['asks'])
        })

        # Perp
        ob_perp = futures_client.fetch_order_book(symbol, limit=limit)
        ts_perp_raw = ob_perp.get('timestamp')
        ts_perp = pd.to_datetime(ts_perp_raw, unit='ms') if ts_perp_raw else pd.Timestamp.utcnow()
        rows.append({
            'timestamp': ts_perp,
            'market': 'perp',
            'mid': mid_from_order_book(ob_perp['bids'], ob_perp['asks']),
            'spread': spread_top(ob_perp['bids'], ob_perp['asks'])
        })

        time.sleep(sleep_s)

    return pd.DataFrame(rows)

# def poll_order_books(spot_client, futures_client, symbol: str,
#                      limit: int = 50, n: int = 100, sleep_s: float = 0.5) -> pd.DataFrame:
#     """
#     Poll both Spot and Futures order books n times and compute mid and spread at each snapshot.
#     Returns a combined DataFrame with market labels.
#     """
#     rows = []
#     for _ in range(n):
#         # Spot
#         ob_spot = spot_client.fetch_order_book(symbol, limit=limit)
#         mid_spot = mid_from_order_book(ob_spot['bids'], ob_spot['asks'])
#         spr_spot = spread_top(ob_spot['bids'], ob_spot['asks'])
#         rows.append({
#             'timestamp': pd.to_datetime(ob_spot['timestamp'], unit='ms'),
#             'market': 'spot',
#             'mid': mid_spot,
#             'spread': spr_spot
#         })

#         # Futures
#         ob_perp = futures_client.fetch_order_book(symbol, limit=limit)
#         mid_perp = mid_from_order_book(ob_perp['bids'], ob_perp['asks'])
#         spr_perp = spread_top(ob_perp['bids'], ob_perp['asks'])
#         rows.append({
#             'timestamp': pd.to_datetime(ob_perp['timestamp'], unit='ms'),
#             'market': 'perp',
#             'mid': mid_perp,
#             'spread': spr_perp
#         })

#         time.sleep(sleep_s)

#     return pd.DataFrame(rows)

# Example usage
# symbol = 'BTCUSDT'
# combined_data = poll_order_books(spot, futures, symbol, limit=50, n=5, sleep_s=0.5)
# print(combined_data)

#to compare spot vs perp, we use dual function below
# combined = poll_order_books(spot.client, futures.client, PAIR_SPOT, limit=SNAPSHOT_DEPTH, n=5)
# combined.to_csv(os.path.join(BASE_DIR, "data", "samples", "poll_dual.csv"), index=False)
# log.info(f"Collected {len(combined)} combined spot/perp snapshots")

