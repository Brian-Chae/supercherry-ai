from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.trading_account import TradingAccount
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/api/system", tags=["system"])


@router.get("/status")
def get_system_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """시스템 상태 조회"""
    # 활성 거래 계정 수
    active_accounts = db.query(TradingAccount).filter(
        TradingAccount.user_id == current_user.id,
        TradingAccount.is_active == True
    ).count()
    
    # API 연결 상태 (간단한 체크)
    api_status = "connected" if active_accounts > 0 else "disconnected"
    
    return {
        "api_status": api_status,
        "active_accounts": active_accounts,
        "user_id": current_user.id
    }

