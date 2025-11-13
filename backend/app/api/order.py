from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.trading_account import TradingAccount
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderResponse
from app.api.dependencies import get_current_user
from app.services.kis_api import KISAPIClient

router = APIRouter(prefix="/api/order", tags=["order"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """주문 생성"""
    # 거래 계정 확인
    trading_account = db.query(TradingAccount).filter(
        TradingAccount.id == order.trading_account_id,
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
        
        # 주문 타입 변환
        order_type_code = "02" if order.order_type == "BUY" else "01"
        order_method_code = "01" if order.order_method == "MARKET" else "00"
        
        # 한국투자증권 API로 주문 실행
        result = client.place_order(
            account_number=trading_account.account_number,
            symbol=order.symbol,
            order_type=order.order_type,
            quantity=order.quantity,
            price=int(order.price) if order.price else None,
            order_method=order_method_code
        )
        
        # DB에 주문 저장
        db_order = Order(
            user_id=current_user.id,
            trading_account_id=order.trading_account_id,
            symbol=order.symbol,
            order_type=order.order_type,
            order_method=order.order_method,
            quantity=order.quantity,
            price=order.price,
            status="PENDING",
            strategy_id=order.strategy_id,
            order_metadata=order.metadata
        )
        
        if "output" in result and "ODNO" in result["output"]:
            db_order.kis_order_no = result["output"]["ODNO"]
        
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        return db_order
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to place order: {str(e)}"
        )


@router.get("", response_model=list[OrderResponse])
def get_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """주문 내역 조회"""
    orders = db.query(Order).filter(
        Order.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return orders

