from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class KISToken(Base):
    __tablename__ = "kis_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    trading_account_id = Column(Integer, ForeignKey("trading_accounts.id"), nullable=False)
    access_token = Column(String, nullable=False)
    token_type = Column(String, default="Bearer")
    issued_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_in = Column(Integer, default=86400)  # 24 hours in seconds
    
    # Relationships
    trading_account = relationship("TradingAccount", back_populates="kis_tokens")

