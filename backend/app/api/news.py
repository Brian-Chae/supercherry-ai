from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.user import User
from app.models.trading_account import TradingAccount
from app.api.dependencies import get_current_user
from app.services.kis_api import KISAPIClient

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("")
def get_news(
    symbol: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """뉴스 조회"""
    # 사용자의 활성 계정 조회
    trading_account = db.query(TradingAccount).filter(
        TradingAccount.user_id == current_user.id,
        TradingAccount.is_active == True
    ).first()
    
    if not trading_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trading account not found"
        )
    
    try:
        client = KISAPIClient(trading_account, db)
        result = client.get_news(symbol)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get news: {str(e)}"
        )

