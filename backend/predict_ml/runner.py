from loguru import logger
import pandas as pd
import os, sys

# Add parent directory to path
module_path = os.path.abspath(os.path.join('.'))
if module_path not in sys.path:
    sys.path.append(module_path)
    
from backend.model.model_service import ModelService
from backend.model.pipeline.collection import get_data
from pred_chart import plot_predictions

@logger.catch
def main(symbol, interval, forecast_period):
    logger.info('Running the application...')
    
    df = get_data(symbol, interval, forecast_period)
    X_future = df.drop(['Prediction'], axis=1)[-forecast_period:]
    
    ml_svc = ModelService(df, forecast_period)
    model = ml_svc.load_model()
    
    prediction = model.predict(X_future)
    print(pd.Series(prediction))
    fig = plot_predictions(df, forecast_period, prediction, symbol, interval)
    fig.show()
    
    
if __name__ == '__main__':
    main('BTCUSDT', '1h', 15)