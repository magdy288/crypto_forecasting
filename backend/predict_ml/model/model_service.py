from loguru import logger
import pandas as pd
import pickle as pk
import os, sys

# Add parent directory to path
module_path = os.path.abspath(os.path.join('.'))
if module_path not in sys.path:
    sys.path.append(module_path)
    
from backend.predict_ml.config.model import model_settings
from backend.predict_ml.model.pipeline.model import Model
from backend.predict_ml.model.pipeline.collection import get_data


model_dir = model_settings.ml_path
model_name = model_settings.ml_name
full_path = os.path.join(model_dir, model_name)

class ModelService:
    def __init__(
        self,
        df: pd.DataFrame,
        forecast_period: int,
    ):
        self.model = None
        self.df = df
        self.forecast_period = forecast_period
        
    def load_model(self):
        model_obj = Model(self.df, self.forecast_period)
        model_obj.build_model()
        
        logger.info(f'Loading model from {full_path}')
        with open(full_path, 'rb') as f:
            self.model = pk.load(f)
        
        return self.model
    

if __name__ == '__main__':
    forcast_n = 50
    symbol = 'BNBUSDT'
    df = get_data(symbol, '1h', forcast_n)
    X_future = df.drop(['Prediction'], axis=1)[-forcast_n:]

    service = ModelService(df, forcast_n)
    rf_v1 = service.load_model()
    prediction = rf_v1.predict(X_future)
    print(prediction)