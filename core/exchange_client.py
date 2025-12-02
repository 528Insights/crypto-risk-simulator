import ccxt
import time
import logging
from datetime import datetime

log = logging.getLogger(__name__)

class ExchangeClient:
    def __init__(self, market_type="spot", timeout=30000, retries=3, delay=2):
        """
        Initialize a Binance client with extended timeout and retry logic.
        market_type: "spot" or "perp"
        timeout: request timeout in ms (default 30s)
        retries: number of retry attempts on timeout
        delay: seconds to wait between retries
        """
        if market_type == "spot":
            self.client = ccxt.binance({
                'enableRateLimit': True,
                'timeout': timeout
            })
        elif market_type == "perp":
            self.client = ccxt.binance({
                'options': {'defaultType': 'future'},
                'enableRateLimit': True,
                'timeout': timeout
            })
        else:
            raise ValueError("market_type must be 'spot' or 'perp'")

        self.retries = retries
        self.delay = delay

    def _retry_call(self, func, *args, **kwargs):
        """
        Internal helper: wrap ccxt calls with retry logic.
        """
        for attempt in range(self.retries):
            try:
                return func(*args, **kwargs)
            except ccxt.RequestTimeout:
                log.warning(f"Timeout on {func.__name__} (attempt {attempt+1}/{self.retries})")
                time.sleep(self.delay)
            except Exception as e:
                log.error(f"Unexpected error in {func.__name__}: {e}")
                raise
        raise RuntimeError(f"Failed {func.__name__} after {self.retries} retries")

    def order_book(self, pair: str, limit: int = 50):
        """
        Fetch order book for a trading pair.
        Returns dict with bids and asks.
        """
        return self._retry_call(self.client.fetch_order_book, pair, limit)

    def ohlcv(self, pair: str, timeframe: str = '1h', limit: int = 100):
        """
        Fetch OHLCV candles for a trading pair.
        Returns list of [timestamp, open, high, low, close, volume].
        """
        return self._retry_call(self.client.fetch_ohlcv, pair, timeframe, limit)

    def print_order_book(self, pair: str, limit: int = 5):
        """
        Utility: print top bids/asks for debugging.
        """
        ob = self.order_book(pair, limit=limit)
        print(f"Top {limit} bids:", ob['bids'][:limit])
        print(f"Top {limit} asks:", ob['asks'][:limit])

    def print_ohlcv(self, pair: str, timeframe: str = '1h', limit: int = 5):
        """
        Utility: print OHLCV candles for debugging.
        """
        ohlcv = self.ohlcv(pair, timeframe=timeframe, limit=limit)
        print(f"\n{pair} OHLCV:")
        for c in ohlcv:
            ts = datetime.utcfromtimestamp(c[0]/1000)
            print(ts, c[1], c[2], c[3], c[4], c[5])









# Spot client
# spot = ccxt.binance()

# # Futures client
# futures = ccxt.binance({'options': {'defaultType': 'future'}})

# # Spot order book
# spot_ob = spot.fetch_order_book('BTCUSDT', limit=50)
# print("Spot top 5 bids:", spot_ob['bids'][:5])
# print("Spot top 5 asks:", spot_ob['asks'][:5])

# # Futures order book
# perp_ob = futures.fetch_order_book('BTCUSDT', limit=50)
# print("Perp top 5 bids:", perp_ob['bids'][:5])
# print("Perp top 5 asks:", perp_ob['asks'][:5])

# # Spot OHLCV
# spot_ohlcv = spot.fetch_ohlcv('BTCUSDT', timeframe='1h', limit=5)
# print("\nSpot OHLCV:")
# for c in spot_ohlcv:
#     ts = datetime.utcfromtimestamp(c[0]/1000)
#     print(ts, c[1], c[2], c[3], c[4], c[5])

# # Futures OHLCV
# perp_ohlcv = futures.fetch_ohlcv('BTCUSDT', timeframe='1h', limit=5)
# print("\nPerp OHLCV:")
# for c in perp_ohlcv:
#     ts = datetime.utcfromtimestamp(c[0]/1000)
#     print(ts, c[1], c[2], c[3], c[4], c[5])
