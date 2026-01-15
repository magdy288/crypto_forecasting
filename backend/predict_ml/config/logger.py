from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class LoggerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='./backend/predict_ml/config/.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )
    
    log_level: str
    
def configure_logging(log_level: str) -> None:
    logger.remove()
    logger.add(
        './backend/predict_ml/logs/app.log',
        rotation='1 day',
        retention='2 days',
        compression='zip',
        level=log_level
    )

def main():
    settings = LoggerSettings()
    configure_logging(settings.log_level)
    
if __name__ == "__main__":
    main()