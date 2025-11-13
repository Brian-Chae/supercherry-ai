from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Balance(Base):
    __tablename__ = "balances"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trading_account_id = Column(Integer, ForeignKey("trading_accounts.id"), nullable=False)
    
    # Balance details
    symbol = Column(String, nullable=False)  # 종목코드
    quantity = Column(Integer, nullable=False)
    average_price = Column(Float, nullable=False)
    current_price = Column(Float)
    total_value = Column(Float)  # 현재 평가금액
    profit_loss = Column(Float)  # 평가손익
    profit_loss_rate = Column(Float)  # 수익률 (%)
    
    # Snapshot time
    snapshot_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")

