import os, sys
print("Working directory:", os.getcwd())
print("Python path:", sys.path)

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import numpy as np
from core.exchange_client import ExchangeClient
from core.market_data import depth_snapshot, mid_from_order_book
from core.ndf_pricer import make_ndf_quote
from core.execution import vwap_execute, twap_execute
from core.microprice_simulator import microprice_path
from core.risk import historical_var, stress_scenarios
from config import EXCHANGE_SPOT, PAIR_SPOT, EXCHANGE_PERP, PAIR_PERP, SEED

#----------------- Page Setup--------------
st.set_page_config(page_title='Crypto Desk Simulator', layout='wide')
st.title('Crypto Derivatives Liquidity & Risk Simulator')

# ---------------- Market Selection ----------------
market_option = st.radio(
    "Select Market to Display",
    ('Spot', 'Perp', 'Both'),
    index=2
)

# ---------------- Initialise Clients ----------------
spot_client = ExchangeClient(EXCHANGE_SPOT)
perp_client = ExchangeClient(EXCHANGE_PERP)

def get_mid_and_snapshot(client, pair):
    ob = client.order_book(pair, limit=50)
    mid = mid_from_order_book(ob['bids'], ob['asks'])
    snap = depth_snapshot(ob['bids'], ob['asks'], depth=20)
    return ob, mid, snap

# Spot data
ob_spot, mid_spot, snap_spot = get_mid_and_snapshot(spot_client, PAIR_SPOT)
# Perp data
ob_perp, mid_perp, snap_perp = get_mid_and_snapshot(perp_client, PAIR_PERP)

# ---------------- Display Order Book ----------------
st.subheader('Order Book Depth')

if market_option in ('Spot', 'Both'):
    st.write('Spot')
    st.bar_chart(snap_spot.pivot_table(index='price', columns='side', values='size', aggfunc='sum'))
    st.metric(label='Mid price (Spot)', value=f'{mid_spot:,.2f}')
    st.metric(label='Spread (Spot)', value=f'{ob_spot["asks"][0][0] - ob_spot["bids"][0][0]:.2f}')

if market_option in ('Perp', 'Both'):
    st.write('Perp')
    st.bar_chart(snap_perp.pivot_table(index='price', columns='side', values='size', aggfunc='sum'))
    st.metric(label='Mid price (Perp)', value=f'{mid_perp:,.2f}')
    st.metric(label='Spread (Perp)', value=f'{ob_perp["asks"][0][0] - ob_perp["bids"][0][0]:.2f}')

st.markdown('---')

# ---------------- NDF Pricing ----------------
st.subheader('OTC NDF Quote (1W)')
r_annual = st.slider('r (annual)', 0.0, 0.15, 0.05, 0.01)
q_annual = st.slider('q (annual)', 0.0, 0.15, 0.02, 0.01)
spread_bp = st.slider('Dealer spread (bp)', 5, 50, 25, 5)

if market_option in ('Spot', 'Both'):
    ndf_spot = make_ndf_quote(mid_spot, r_annual, q_annual, tenor_days=7, spread_bp=spread_bp)
    st.write(f'Spot Forward: {ndf_spot.forward:,.2f} | Bid: {ndf_spot.bid:,.2f} | Ask: {ndf_spot.ask:,.2f}')

if market_option in ('Perp', 'Both'):
    ndf_perp = make_ndf_quote(mid_perp, r_annual, q_annual, tenor_days=7, spread_bp=spread_bp)
    st.write(f'Perp Forward: {ndf_perp.forward:,.2f} | Bid: {ndf_perp.bid:,.2f} | Ask: {ndf_perp.ask:,.2f}')

st.markdown('---')

# ---------------- Block Trade Execution ----------------
st.subheader('Block Trade Execution Simulator')
target_notional = st.slider('Target notional (USD)', 10_000, 500_000, 100_000, 10_000)

def run_execution(mid_price):
    qty = target_notional / mid_price
    path = microprice_path(mid_price, n=60, sigma_bp=30, seed=SEED)
    volumes = np.random.default_rng(SEED).integers(1, 20, size=60)
    vwap_res = vwap_execute(path, volumes, qty)
    twap_res = twap_execute(path, qty)
    return path, vwap_res, twap_res

if market_option in ('Spot', 'Both'):
    path_spot, vwap_spot, twap_spot = run_execution(mid_spot)
    st.write(f'Spot VWAP avg: {vwap_spot.avg_price:,.2f} | Slippage: {vwap_spot.slippage_bps:.1f} bp')
    st.write(f'Spot TWAP avg: {twap_spot.avg_price:,.2f} | Slippage: {twap_spot.slippage_bps:.1f} bp')

if market_option in ('Perp', 'Both'):
    path_perp, vwap_perp, twap_perp = run_execution(mid_perp)
    st.write(f'Perp VWAP avg: {vwap_perp.avg_price:,.2f} | Slippage: {vwap_perp.slippage_bps:.1f} bp')
    st.write(f'Perp TWAP avg: {twap_perp.avg_price:,.2f} | Slippage: {twap_perp.slippage_bps:.1f} bp')

# ---------------- Microprice Chart ----------------
chart_data = {}
if market_option in ('Spot', 'Both'):
    chart_data['Spot Microprice'] = path_spot
if market_option in ('Perp', 'Both'):
    chart_data['Perp Microprice'] = path_perp
st.line_chart(pd.DataFrame(chart_data))

st.markdown('---')


# ---------------- Risk Metrics ----------------
st.subheader('Risk Metrics')

if market_option in ('Spot', 'Both'):
    ohlcv_spot = spot_client.ohlcv(PAIR_SPOT, timeframe='1h', limit=24*250)
    df_spot = pd.DataFrame(ohlcv_spot, columns=['ts','open','high','low','close','vol'])
    df_spot['ret'] = df_spot['close'].pct_change()
    daily_spot = df_spot['ret'].rolling(24).sum().dropna()
    var_99_spot = historical_var(daily_spot, alpha=0.99, notional=target_notional)
    st.write(f'Spot 99% VaR: ${var_99_spot:,.0f}')
    
    stress_spot = stress_scenarios(current_price=mid_spot, position_qty=target_notional/mid_spot)
    st.write('Spot Stress Scenarios')
    st.dataframe(stress_spot)
    st.bar_chart(stress_spot.set_index('Shock')['Net PnL'])

if market_option in ('Perp', 'Both'):
    ohlcv_perp = perp_client.ohlcv(PAIR_PERP, timeframe='1h', limit=24*250)
    df_perp = pd.DataFrame(ohlcv_perp, columns=['ts','open','high','low','close','vol'])
    df_perp['ret'] = df_perp['close'].pct_change()
    daily_perp = df_perp['ret'].rolling(24).sum().dropna()
    var_99_perp = historical_var(daily_perp, alpha=0.99, notional=target_notional)
    st.write(f'Perp 99% VaR: ${var_99_perp:,.0f}')
    
    stress_perp = stress_scenarios(current_price=mid_perp, position_qty=target_notional/mid_perp)
    st.write('Perp Stress Scenarios')
    st.dataframe(stress_perp)
    st.bar_chart(stress_perp.set_index('Shock')['Net PnL'])

# st.subheader('Risk Metrics')

# if market_option in ('Spot', 'Both'):
#     ohlcv_spot = spot_client.ohlcv(PAIR_SPOT, timeframe='1h', limit=24*250)
#     df_spot = pd.DataFrame(ohlcv_spot, columns=['ts','open','high','low','close','vol'])
#     df_spot['ret'] = df_spot['close'].pct_change()
#     daily_spot = df_spot['ret'].rolling(24).sum().dropna()
#     var_99_spot = historical_var(daily_spot, alpha=0.99, notional=target_notional)
#     st.write(f'Spot 99% VaR: ${var_99_spot:,.0f}')
    
#     stress_spot = stress_scenarios(current_price=mid_spot, position_qty=target_notional/mid_spot)
#     st.write('Spot Stress Scenarios')
#     st.dataframe(stress_spot)
#     st.bar_chart(stress_spot.set_index('shock_pct')['pnl'])

# if market_option in ('Perp', 'Both'):
#     ohlcv_perp = perp_client.ohlcv(PAIR_PERP, timeframe='1h', limit=24*250)
#     df_perp = pd.DataFrame(ohlcv_perp, columns=['ts','open','high','low','close','vol'])
#     df_perp['ret'] = df_perp['close'].pct_change()
#     daily_perp = df_perp['ret'].rolling(24).sum().dropna()
#     var_99_perp = historical_var(daily_perp, alpha=0.99, notional=target_notional)
#     st.write(f'Perp 99% VaR: ${var_99_perp:,.0f}')
    
#     stress_perp = stress_scenarios(current_price=mid_perp, position_qty=target_notional/mid_perp)
#     st.write('Perp Stress Scenarios')
#     st.dataframe(stress_perp)
#     st.bar_chart(stress_perp.set_index('shock_pct')['pnl'])


