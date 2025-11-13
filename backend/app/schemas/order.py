from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime


class OrderCreate(BaseModel):
    trading_account_id: int
    symbol: str
    order_type: str  # BUY, SELL
    order_method: str  # MARKET, LIMIT
    quantity: int
    price: Optional[float] = None
    strategy_id: Optional[int] = None
    metadata: Optional[Dict] = {}


class OrderResponse(BaseModel):
    id: int
    symbol: str
    order_type: str
    order_method: str
    quantity: int
    price: Optional[float]
    executed_price: Optional[float]
    executed_quantity: int
    status: str
    kis_order_no: Optional[str]
    strategy_id: Optional[int]
    order_metadata: Optional[Dict] = {}
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

