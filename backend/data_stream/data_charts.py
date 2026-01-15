import plotly.graph_objects as go
from plotly.subplots import make_subplots
from fh_plotly import plotly2fasthtml
from datetime import datetime
import httpx
import pandas as pd

def compute_bbands(series, period=20, std=2):
    sma = series.rolling(period).mean()
    dev = series.rolling(period).std()
    upper = sma + std * dev
    lower = sma - std * dev
    return sma, upper, lower

def compute_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    hist = macd - signal_line
    return macd, signal_line, hist

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def create_ohlcv_chart(symbol, data, indicators):
    df = pd.DataFrame(
        data,
        columns=["time", "open", "high", "low", "close", "volume"]
    )

    rows = 2
    if "rsi" in indicators:
        rows += 1
    if "macd" in indicators:
        rows += 1

    fig = make_subplots(
        rows=rows,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_width=[0.2] * (rows - 1) + [0.6],
    )

    row_idx = 1

    # === Candlestick ===
    fig.add_trace(go.Candlestick(
        x=df["time"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="Price"
    ), row=row_idx, col=1)

    # === Bollinger Bands ===
    if "bbands" in indicators:
        sma, upper, lower = compute_bbands(df["close"])

        fig.add_trace(go.Scatter(
            x=df["time"], y=upper, line=dict(width=1),
            name="BB Upper"
        ), row=row_idx, col=1)

        fig.add_trace(go.Scatter(
            x=df["time"], y=lower, line=dict(width=1),
            name="BB Lower", fill="tonexty", opacity=0.2
        ), row=row_idx, col=1)

    row_idx += 1

    # === Volume ===
    fig.add_trace(go.Bar(
        x=df["time"],
        y=df["volume"],
        name="Volume"
    ), row=row_idx, col=1)

    # === RSI ===
    if "rsi" in indicators:
        row_idx += 1
        rsi = compute_rsi(df["close"])

        fig.add_trace(go.Scatter(
            x=df["time"], y=rsi, name="RSI"
        ), row=row_idx, col=1)

        fig.add_hline(y=70, line_dash="dash", row=row_idx, col=1)
        fig.add_hline(y=30, line_dash="dash", row=row_idx, col=1)

    # === MACD ===
    if "macd" in indicators:
        row_idx += 1
        macd, signal, hist = compute_macd(df["close"])

        fig.add_trace(go.Bar(
            x=df["time"], y=hist, name="MACD Hist"
        ), row=row_idx, col=1)

        fig.add_trace(go.Scatter(
            x=df["time"], y=macd, name="MACD"
        ), row=row_idx, col=1)

        fig.add_trace(go.Scatter(
            x=df["time"], y=signal, name="Signal"
        ), row=row_idx, col=1)

    fig.update_layout(
        title=f"{symbol} Real-Time OHLCV",
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        height=250 + 150 * rows,
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return plotly2fasthtml(fig)

async def fetch_ohlcv(symbol: str = 'BTCUSDT', interval: str = '1m'):
    """Fetch recent candles using httpx."""
    BINANCE_URL = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=30"
    
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(BINANCE_URL)
            return [
                [datetime.fromtimestamp(c[0]/1000).strftime('%H:%M'), 
                 float(c[1]), float(c[2]), float(c[3]), float(c[4]), float(c[5])] 
                for c in r.json()
            ]
        except Exception as e:
            print(f"Fetch error: {e}")
            return None