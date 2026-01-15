from loguru import logger
from pydantic import DirectoryPath, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv()

class ModelSettings(BaseSettings):
    ml_path : DirectoryPath = Field(..., description="The path to the ML model directory.")
    ml_name: str = Field(..., description="Name of the ML model.")
    
    model_config = SettingsConfigDict(
        env_file='./backend/predict_ml/config/.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    

    

model_settings = ModelSettings(
    ml_path=os.getenv('MODEL_PATH'),
    ml_name=os.getenv('ML_NAME')
)

# # Ensure the path exists
# if not os.path.exists(model_settings.ml_path):
#     raise FileNotFoundError(f"The provided ML directory path ({model_settings.ml_path}) does not exist.")

