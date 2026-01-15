from sqlalchemy import DateTime, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from pathlib import Path
import os, sys

# Add parent directory to path
module_path = os.path.abspath(os.path.join('.'))
if module_path not in sys.path:
    sys.path.append(module_path)
    
# Now you can import from parent directory
from backend.predict_ml.config.db_config import db_settings



class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass

class CryptoData(Base):
    __tablename__ = Path(db_settings.crypto_table_name).stem

    
    timestamp: Mapped[datetime] = mapped_column(DateTime, primary_key=True)
    Open: Mapped[float] = mapped_column(Float())
    High: Mapped[float] = mapped_column(Float())
    Low: Mapped[float] = mapped_column(Float())
    Close: Mapped[float] = mapped_column(Float())
    Volume: Mapped[float] = mapped_column(Float())
    S_SMA: Mapped[float] = mapped_column(Float())
    f_SMA: Mapped[float] = mapped_column(Float())
    RSI: Mapped[float] = mapped_column(Float())
    Prediction: Mapped[float] = mapped_column(Float())