from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.api import auth, market, order, balance, news, strategy, system, trading_account, kis_test
import logging

logger = logging.getLogger(__name__)

# 데이터베이스 테이블 생성 (연결 실패 시 무시)
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.warning(f"Failed to create database tables: {e}. Please ensure PostgreSQL is running and DATABASE_URL is correct.")

app = FastAPI(
    title="ETF 자동매매 시스템",
    description="한국투자증권 API를 이용한 ETF 자동매매 시스템",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(auth.router)
app.include_router(market.router)
app.include_router(order.router)
app.include_router(balance.router)
app.include_router(news.router)
app.include_router(strategy.router)
app.include_router(system.router)
app.include_router(trading_account.router)
app.include_router(kis_test.router)  # KIS API 테스트용


@app.get("/")
def root():
    return {"message": "ETF 자동매매 시스템 API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

