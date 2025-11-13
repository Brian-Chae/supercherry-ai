from pydantic import BaseModel
from datetime import datetime


class TradingAccountCreate(BaseModel):
    account_number: str
    app_key: str
    app_secret: str


class TradingAccountResponse(BaseModel):
    id: int
    account_number: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

