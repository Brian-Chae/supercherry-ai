#!/usr/bin/env python3
"""
테스트 사용자 생성 스크립트
사용법: python scripts/create-test-user.py
"""
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# 환경 변수 로드
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from app.database import SessionLocal, Base
from app.models.user import User
from app.services.auth_service import get_user_by_username, create_user
from app.schemas.user import UserCreate
from app.config import settings

def create_test_user():
    """테스트 사용자 생성"""
    # 데이터베이스 URL에서 데이터베이스 이름 추출
    db_url = settings.DATABASE_URL
    # postgresql://user:pass@host:port/dbname 형식에서 dbname 추출
    if '/etf_trading' in db_url:
        # 기본 PostgreSQL 연결 (데이터베이스 없이)
        base_url = db_url.rsplit('/', 1)[0] + '/postgres'
        admin_engine = create_engine(base_url)
        
        # 데이터베이스가 없으면 생성
        try:
            with admin_engine.connect() as conn:
                conn.execute(text("COMMIT"))
                conn.execute(text(f'CREATE DATABASE "{settings.DATABASE_URL.split("/")[-1]}"'))
                print("✅ 데이터베이스가 생성되었습니다.")
        except Exception as e:
            if "already exists" not in str(e).lower():
                print(f"⚠️  데이터베이스 생성 시도 중 오류 (이미 존재할 수 있음): {e}")
        finally:
            admin_engine.dispose()
    
    # 실제 데이터베이스 연결
    from app.database import engine
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"⚠️  데이터베이스 연결 오류: {e}")
        print("   데이터베이스가 실행 중인지 확인하세요: docker-compose -f docker-compose.dev.yml ps")
        return
    
    db: Session = SessionLocal()
    try:
        # 기본 테스트 사용자 정보
        test_username = "testuser"
        test_email = "test@example.com"
        test_password = "test1234"
        
        # 이미 존재하는지 확인
        existing_user = get_user_by_username(db, test_username)
        if existing_user:
            print(f"⚠️  사용자 '{test_username}'가 이미 존재합니다.")
            print(f"   이메일: {existing_user.email}")
            return
        
        # 사용자 생성
        user_data = UserCreate(
            username=test_username,
            email=test_email,
            password=test_password
        )
        
        user = create_user(db, user_data)
        print("✅ 테스트 사용자가 생성되었습니다!")
        print(f"   사용자명: {user.username}")
        print(f"   이메일: {user.email}")
        print(f"   비밀번호: {test_password}")
        print("\n💡 로그인 페이지에서 위 정보를 사용하여 로그인하세요.")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()

