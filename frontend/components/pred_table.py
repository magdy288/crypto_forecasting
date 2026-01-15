import pandas as pd


# Helper function to create prediction series table
def create_prediction_series(df, interval: str, forecast_period: int, prediction):
    last_date = df.index[-1]
    tz = getattr(df.index, 'tz', None)
    if 'd' in interval:
        delta = pd.Timedelta(days=1)
        period = 'D'
    elif 'h' in interval:
        delta = pd.Timedelta(hours=1)
        period = 'H'
    elif 'm' in interval:
        delta = pd.Timedelta(minutes=1)
        period = 'T'
    pred_dates = pd.date_range(last_date + delta, periods=forecast_period, freq=period, tz=tz)
    
    pred_series = pd.DataFrame({
        'Price': prediction,
        'Date': pred_dates
    })
    return pred_series