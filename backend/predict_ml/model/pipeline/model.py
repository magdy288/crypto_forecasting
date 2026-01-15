from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from loguru import logger
import pandas as pd
import pickle as pk
import os, sys


# Add parent directory to path
module_path = os.path.abspath(os.path.join('.'))
if module_path not in sys.path:
    sys.path.append(module_path)

from backend.predict_ml.config.model import model_settings


## File Pathes
model_dir = model_settings.ml_path
model_name = model_settings.ml_name

class Model:
    def __init__(self, df: pd.DataFrame, forecast_period: int = 30):
        self.forecast_period = forecast_period
        self.df = df
        
    def build_model(self):
        logger.info('Starting up model building pipeline')
        X, y = self._get_x_y()
        
        X_train, X_test, y_train, y_test = self._split_train_test(
            X, 
            y
        )
        
        rf = self._train_model(
            X_train, 
            y_train
        )
        
        self._evaluate_model(
            rf,
            X_test,
            y_test,
        )
        self._save_model(rf)
        
    def _get_x_y(self):
        self.df['Prediction'] = self.df[['Close']].shift(-self.forecast_period)

        X = self.df.drop(['Prediction'], axis=1)[:-self.forecast_period]
        y = self.df['Prediction'][:-self.forecast_period]

        logger.info(f'defining X and Y Variables.')
        return X, y
    
    def _split_train_test(
        self, 
        X: pd.DataFrame, 
        y: pd.Series,
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        
        logger.info('Splitting data into train and test sets')
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
        return X_train, X_test, y_train, y_test
    
    def _train_model(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
    ) -> RandomForestRegressor:
        
        logger.info('Training a model with hyperparameters')
        grid_space = {
            'n_estimators': [100, 150, 200, 250],
            'max_depth': [6, 9, 12],
        }
        
        grid = GridSearchCV(RandomForestRegressor(),
                            param_grid=grid_space, cv=5, scoring='r2')
        
        model_grid = grid.fit(X_train, y_train)
        
        return model_grid.best_estimator_
    
    def _evaluate_model(
        self,
        model: RandomForestRegressor,
        X_test: pd.DataFrame,
        y_test: pd.Series,
    ) -> float:
        
        model_score = model.score(
            X_test,
            y_test
        )
        logger.info(f'Evaluating model performance. SCORE={model_score}')
        return model_score
    
    def _save_model(
        self,
        model: RandomForestRegressor,
    ):
        os.makedirs(model_dir, exist_ok=True)
        full_path = os.path.join(model_dir, model_name)
        
        # remove existing file if present
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
            except Exception:
                logger.exception('Could not remove existing model file')
        
        logger.info(f'Saving a model to a directory: {full_path}')
        with open(full_path, 'wb') as f:
            pk.dump(model, f)

        return full_path
  
  
    
# forcast_n = 50
# df = get_data('SOLUSDT', '1d', forcast_n)

# service = Model(df, forcast_n)
# service.build_model()