import plotly.graph_objects as go
import pandas as pd
import numpy as np


def plot_predictions(df_plot, future_period, future_predictions, symbol: str, interval: str):
    last_date = df_plot.index[-1]
    tz = getattr(df_plot.index, 'tz', None)

    


    # Choose a timedelta step for the selected period
    if 'd' in interval:
        delta = pd.Timedelta(days=1)
        period = 'D'
    elif 'h' in interval:
        delta = pd.Timedelta(hours=1)
        period = 'H'
    elif 'm' in interval:
        delta = pd.Timedelta(minutes=1)
        period = 'T'

    # Build future date range with same tz as original index
    future_dates = pd.date_range(last_date + delta, periods=future_period, freq=period, tz=tz)

    # Infer base width from historical index frequency (use median diff)
    if len(df_plot.index) > 1:
        median_delta = df_plot.index.to_series().diff().median()
        if pd.isnull(median_delta):
            median_delta = pd.Timedelta(minutes=1)
    else:
        median_delta = pd.Timedelta(minutes=1)


    fig = go.Figure()

    # Add historical candlestick (Plotly Candlestick does not accept 'width')
    fig.add_trace(go.Candlestick(
        x=df_plot.index,
        open=df_plot['Open'],
        high=df_plot['High'],
        low=df_plot['Low'],
        close=df_plot['Close'],
        name='Historical OHLC',
        increasing_line_color='#26a69a',
        decreasing_line_color='#ef553b',
    ))

    # Create synthetic OHLC candlesticks for predictions (keep shapes reasonable for smaller timeframes)
    pred_close = np.array(future_predictions, dtype=float)
    # Scale the ranges based on recent volatility instead of fixed 2% when high frequency
    recent_vol = (df_plot['High'] - df_plot['Low']).tail(20).median()
    if pd.isnull(recent_vol) or recent_vol == 0:
        recent_vol = (df_plot['Close'].pct_change().abs().median() or 0.01) * df_plot['Close'].iloc[-1]

    # Use fraction of recent_vol for minute/hour charts, and percent otherwise
    if period in ('T', 'H'):
        range_scale = recent_vol * 0.6
    else:
        range_scale = pred_close * 0.02

    pred_high = pred_close + range_scale
    pred_low = pred_close - range_scale
    pred_open = pred_close - (range_scale * 0.3)

    fig.add_trace(go.Candlestick(
        x=future_dates,
        open=pred_open,
        high=pred_high,
        low=pred_low,
        close=pred_close,
        name='Predicted OHLC',
        increasing_line_color="#b493d3",
        decreasing_line_color="#6a4c8a",
    ))

    # If you want predicted candles visually narrower, overlay semi-transparent rectangles or use markers instead.

    # Improve layout for dense timeframes
    fig.update_layout(
        title={
            'text': f'Crypto Price Prediction - {symbol} Candlestick Chart',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24}
        },
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        template='plotly_dark',
        hovermode='x unified',
        height=700,
        font=dict(size=12),
        xaxis=dict(
            rangeslider=dict(visible=False),
            type='date',
            tickformatstops=[
                dict(dtickrange=[None, 1000*60], value="%H:%M:%S"),
                dict(dtickrange=[1000*60, 1000*60*60], value="%H:%M"),
                dict(dtickrange=[1000*60*60, 1000*60*60*24], value="%b %d %H:%M"),
                dict(dtickrange=[1000*60*60*24, None], value="%b %d")
            ]
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray'
        ),
        legend=dict(
            x=0.01,
            y=0.99,
            bgcolor='rgba(0,0,0,0.5)',
            bordercolor='gray',
            borderwidth=1
        )
    )

    return fig
