from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime


class StrategyCreate(BaseModel):
    name: str
    strategy_type: str = "VWAP"
    vwap_period: int = 1
    entry_threshold: float = 0.5
    exit_threshold: float = 1.0
    stop_loss_percent: float = 2.0
    take_profit_percent: float = 3.0
    max_holding_days: int = 5
    additional_params: Optional[Dict] = {}


class StrategyUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    vwap_period: Optional[int] = None
    entry_threshold: Optional[float] = None
    exit_threshold: Optional[float] = None
    stop_loss_percent: Optional[float] = None
    take_profit_percent: Optional[float] = None
    max_holding_days: Optional[int] = None
    additional_params: Optional[Dict] = None


class StrategyResponse(BaseModel):
    id: int
    name: str
    strategy_type: str
    is_active: bool
    vwap_period: int
    entry_threshold: float
    exit_threshold: float
    stop_loss_percent: float
    take_profit_percent: float
    max_holding_days: int
    additional_params: Dict
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

