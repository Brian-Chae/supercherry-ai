import httpx
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.config import settings
from app.models.kis_token import KISToken
from app.models.trading_account import TradingAccount
import hashlib
import base64
import json


class KISAPIClient:
    def __init__(self, trading_account: TradingAccount, db: Session):
        self.trading_account = trading_account
        self.db = db
        self.base_url = settings.KIS_BASE_URL
        self.app_key = trading_account.app_key
        self.app_secret = trading_account.app_secret
    
    def _get_or_refresh_token(self) -> str:
        """토큰을 가져오거나 갱신합니다."""
        # DB에서 최신 토큰 조회
        kis_token = self.db.query(KISToken).filter(
            KISToken.trading_account_id == self.trading_account.id
        ).order_by(KISToken.issued_at.desc()).first()
        
        # 토큰이 있고 유효한지 확인
        if kis_token:
            issued_time = kis_token.issued_at
            expires_at = issued_time + timedelta(seconds=kis_token.expires_in)
            now = datetime.now(timezone.utc)
            
            # 만료 5분 전이면 갱신
            if now < expires_at - timedelta(minutes=5):
                return kis_token.access_token
        
        # 새 토큰 발급
        return self._issue_new_token()
    
    def _issue_new_token(self) -> str:
        """새로운 Access Token을 발급합니다."""
        url = f"{self.base_url}/oauth2/tokenP"
        
        headers = {
            "content-type": "application/json"
        }
        
        data = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }
        
        with httpx.Client() as client:
            response = client.post(url, headers=headers, json=data)
            response.raise_for_status()
            token_data = response.json()
        
        # DB에 토큰 저장
        kis_token = KISToken(
            trading_account_id=self.trading_account.id,
            access_token=token_data["access_token"],
            token_type=token_data.get("token_type", "Bearer"),
            expires_in=token_data.get("expires_in", 86400)
        )
        self.db.add(kis_token)
        self.db.commit()
        
        return token_data["access_token"]
    
    def _generate_hashkey(self, data: Dict[str, Any]) -> str:
        """해시키를 생성합니다."""
        data_str = json.dumps(data, separators=(',', ':'))
        hash_input = data_str.encode('utf-8')
        hash_output = hashlib.sha256(hash_input).digest()
        hashkey = base64.b64encode(hash_output).decode('utf-8')
        return hashkey
    
    def _get_headers(self, tr_id: str, use_hash: bool = False, hash_data: Optional[Dict] = None) -> Dict[str, str]:
        """API 요청 헤더를 생성합니다."""
        access_token = self._get_or_refresh_token()
        
        headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {access_token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": tr_id
        }
        
        if use_hash and hash_data:
            headers["hashkey"] = self._generate_hashkey(hash_data)
        
        return headers
    
    def get_current_price(self, symbol: str, market_code: str = "J") -> Dict[str, Any]:
        """현재가를 조회합니다."""
        url = f"{self.base_url}/uapi/domestic-stock/v1/quotations/inquire-price"
        tr_id = "FHKST01010100"
        
        params = {
            "FID_COND_MRKT_DIV_CODE": market_code,  # J: 주식, Q: 코스닥
            "FID_INPUT_ISCD": symbol
        }
        
        headers = self._get_headers(tr_id)
        
        with httpx.Client() as client:
            response = client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
    
    def get_balance(self, account_number: str) -> Dict[str, Any]:
        """계좌 잔고를 조회합니다."""
        url = f"{self.base_url}/uapi/domestic-stock/v1/trading/inquire-balance"
        tr_id = "TTTC8434R"  # 주식 잔고조회
        
        params = {
            "CANO": account_number[:8],  # 계좌번호 앞 8자리
            "ACNT_PRDT_CD": account_number[8:],  # 계좌번호 뒤 2자리
            "AFHR_FLPR_YN": "N",
            "OFL_YN": "",
            "INQR_DVSN": "02",
            "UNPR_DVSN": "01",
            "FUND_STTL_ICLD_YN": "N",
            "FNCG_AMT_AUTO_RDPT_YN": "N",
            "PRCS_DVSN": "01",
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": ""
        }
        
        headers = self._get_headers(tr_id, use_hash=True, hash_data=params)
        
        with httpx.Client() as client:
            response = client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
    
    def place_order(
        self,
        account_number: str,
        symbol: str,
        order_type: str,  # "01": 매도, "02": 매수
        quantity: int,
        price: Optional[int] = None,
        order_method: str = "00"  # "00": 지정가, "01": 시장가
    ) -> Dict[str, Any]:
        """주문을 실행합니다."""
        url = f"{self.base_url}/uapi/domestic-stock/v1/trading/order-cash"
        tr_id = "TTTC0802U"  # 주식 현금 매수 주문
        
        if order_type == "SELL":
            tr_id = "TTTC0801U"  # 주식 현금 매도 주문
            order_type_code = "01"
        else:
            order_type_code = "02"
        
        data = {
            "CANO": account_number[:8],
            "ACNT_PRDT_CD": account_number[8:],
            "PDNO": symbol,
            "ORD_DVSN": order_method,  # "00": 지정가, "01": 시장가
            "ORD_QTY": str(quantity),
            "ORD_UNPR": str(price) if price else "0"
        }
        
        headers = self._get_headers(tr_id, use_hash=True, hash_data=data)
        
        with httpx.Client() as client:
            response = client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
    
    def get_news(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """뉴스를 조회합니다."""
        # 한국투자증권 API의 뉴스 엔드포인트 사용
        # 실제 API 문서에 따라 구현 필요
        url = f"{self.base_url}/uapi/news"
        tr_id = "NEWS001"
        
        params = {}
        if symbol:
            params["symbol"] = symbol
        
        headers = self._get_headers(tr_id)
        
        with httpx.Client() as client:
            response = client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()

