from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Strategy(Base):
    __tablename__ = "strategies"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    strategy_type = Column(String, default="VWAP")  # VWAP, etc.
    is_active = Column(Boolean, default=False)
    
    # VWAP Parameters
    vwap_period = Column(Integer, default=1)  # days
    entry_threshold = Column(Float, default=0.5)  # percentage
    exit_threshold = Column(Float, default=1.0)  # percentage
    stop_loss_percent = Column(Float, default=2.0)  # percentage
    take_profit_percent = Column(Float, default=3.0)  # percentage
    max_holding_days = Column(Integer, default=5)
    
    # Additional parameters as JSON
    additional_params = Column(JSON, default={})
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="strategies")

