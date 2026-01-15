from sqlalchemy import select
from pathlib import Path
from loguru import logger

import pandas as pd
import ccxt
import os, sys

# Add parent directory to path
module_path = os.path.abspath(os.path.join('.'))
if module_path not in sys.path:
    sys.path.append(module_path)
    
from backend.predict_ml.config.db_config import db_settings, engine
from backend.predict_ml.db.db_model import Base, CryptoData

client = ccxt.binance()

def get_data(symbol: str, interval: str, forcast_days: int) -> pd.DataFrame:
    data = client.fetch_ohlcv(symbol, interval, limit=5000)

    df = pd.DataFrame(data, columns=['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df.set_index('timestamp', inplace=True)
    df.index = pd.to_datetime(df.index, unit='ms')
    df.index = df.index.tz_localize('UTC').tz_convert('Africa/Cairo')

    df['S_SMA'] = df['Close'].rolling(window=80).mean()
    df['f_SMA'] = df['Close'].rolling(window=20).mean()
    df['RSI'] = _calculate_rsi(df, 14)

    df.dropna(axis=0, inplace=True)
    
    df['Prediction'] = df[['Close']].shift(-forcast_days)

    # Use sanitized table name (strip any file extension like '.sqlite')
    table_name = Path(db_settings.crypto_table_name).stem

    # Ensure mapped tables exist in the database
    Base.metadata.create_all(engine)

    # query = select(CryptoData)

    df.to_sql(table_name, con=engine, index=True, if_exists='replace')
    logger.info(f'For {symbol} Data saved to database table {table_name}')

    return df


def _calculate_rsi(data, periods=14):
    
    # Calculate price changes
    price_diff = data['Close'].diff()
    # Create gain and loss series
    gain = price_diff.clip(lower=0)
    loss = -1 * price_diff.clip(upper=0)
    # Calculate average gain and loss using rolling mean
    avg_gain = gain.rolling(window=periods).mean()
    avg_loss = loss.rolling(window=periods).mean()
    # Calculate RS and RSI
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

