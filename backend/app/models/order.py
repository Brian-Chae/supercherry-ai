from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trading_account_id = Column(Integer, ForeignKey("trading_accounts.id"), nullable=False)
    
    # Order details
    symbol = Column(String, nullable=False)  # 종목코드
    order_type = Column(String, nullable=False)  # BUY, SELL
    order_method = Column(String, nullable=False)  # MARKET, LIMIT
    quantity = Column(Integer, nullable=False)
    price = Column(Float)  # Limit order price
    executed_price = Column(Float)  # 실제 체결가
    executed_quantity = Column(Integer, default=0)
    
    # Status
    status = Column(String, default="PENDING")  # PENDING, EXECUTED, CANCELLED, PARTIAL
    kis_order_no = Column(String)  # 한국투자증권 주문번호
    
    # Strategy info
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=True)
    
    # Additional data
    order_metadata = Column(JSON, default={})
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="orders")
    trading_account = relationship("TradingAccount", back_populates="orders")

