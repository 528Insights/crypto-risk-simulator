import numpy as np

def microprice_path(mid: float, n: int = 60, sigma_bp: float = 30, seed: int = 42):
    rng = np.random.default_rng(seed)
    shocks = rng.normal(0, sigma_bp/10000.0, size=n) # random shocks in decimal
    path = mid * (1 + shocks).cumprod() # cumulative product simulates price evolution
    return path
