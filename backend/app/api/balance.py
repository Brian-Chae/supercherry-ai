from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.trading_account import TradingAccount
from app.models.balance import Balance
from app.schemas.balance import BalanceResponse
from app.api.dependencies import get_current_user
from app.services.kis_api import KISAPIClient

router = APIRouter(prefix="/api/balance", tags=["balance"])


@router.get("", response_model=list[BalanceResponse])
def get_balance(
    trading_account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """계좌 잔고 조회"""
    # 거래 계정 확인
    trading_account = db.query(TradingAccount).filter(
        TradingAccount.id == trading_account_id,
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
        result = client.get_balance(trading_account.account_number)
        
        # 결과를 Balance 모델로 변환하여 저장
        balances = []
        if "output1" in result:
            for item in result["output1"]:
                balance = Balance(
                    user_id=current_user.id,
                    trading_account_id=trading_account_id,
                    symbol=item.get("pdno", ""),
                    quantity=int(item.get("hldg_qty", 0)),
                    average_price=float(item.get("pchs_avg_pric", 0)),
                    current_price=float(item.get("prpr", 0)) if item.get("prpr") else None,
                    total_value=float(item.get("evlu_amt", 0)) if item.get("evlu_amt") else None,
                    profit_loss=float(item.get("evlu_pfls_amt", 0)) if item.get("evlu_pfls_amt") else None,
                    profit_loss_rate=float(item.get("evlu_pfls_rt", 0)) if item.get("evlu_pfls_rt") else None
                )
                balances.append(balance)
        
        return balances
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get balance: {str(e)}"
        )

