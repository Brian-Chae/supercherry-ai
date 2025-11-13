from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.trading_account import TradingAccount
from app.schemas.trading_account import TradingAccountCreate, TradingAccountResponse
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/api/trading-account", tags=["trading-account"])


@router.post("", response_model=TradingAccountResponse, status_code=status.HTTP_201_CREATED)
def create_trading_account(
    account: TradingAccountCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """거래 계정 생성"""
    db_account = TradingAccount(
        user_id=current_user.id,
        **account.model_dump()
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


@router.get("", response_model=List[TradingAccountResponse])
def get_trading_accounts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """거래 계정 목록 조회"""
    accounts = db.query(TradingAccount).filter(
        TradingAccount.user_id == current_user.id
    ).all()
    return accounts

