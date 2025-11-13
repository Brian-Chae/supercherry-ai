from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BalanceResponse(BaseModel):
    id: int
    symbol: str
    quantity: int
    average_price: float
    current_price: Optional[float]
    total_value: Optional[float]
    profit_loss: Optional[float]
    profit_loss_rate: Optional[float]
    snapshot_at: datetime
    
    class Config:
        from_attributes = True

