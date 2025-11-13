#!/usr/bin/env python3
"""
한국투자증권 API 연결 테스트 스크립트
"""
import sys
import os
import asyncio

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

import httpx
from app.config import settings

async def test_kis_token():
    """KIS API 토큰 발급 테스트"""
    print("🔐 한국투자증권 API 토큰 발급 테스트 중...")
    print(f"   Base URL: {settings.KIS_BASE_URL}")
    print(f"   App Key: {settings.KIS_APP_KEY[:10]}..." if settings.KIS_APP_KEY else "   App Key: (비어있음)")
    print(f"   App Secret: {'***' if settings.KIS_APP_SECRET else '(비어있음)'}")
    print()
    
    if not settings.KIS_APP_KEY or not settings.KIS_APP_SECRET:
        print("❌ KIS_APP_KEY 또는 KIS_APP_SECRET이 설정되지 않았습니다.")
        print("   .env 파일에 다음을 추가하세요:")
        print("   KIS_APP_KEY=your-app-key")
        print("   KIS_APP_SECRET=your-app-secret")
        return False
    
    try:
        async with httpx.AsyncClient() as client:
            # OAuth 2.0 토큰 발급 요청
            response = await client.post(
                f"{settings.KIS_BASE_URL}/oauth2/tokenP",
                headers={
                    "content-type": "application/json"
                },
                json={
                    "grant_type": "client_credentials",
                    "appkey": settings.KIS_APP_KEY,
                    "appsecret": settings.KIS_APP_SECRET
                },
                timeout=10.0
            )
            
            print(f"📡 응답 상태 코드: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 토큰 발급 성공!")
                print(f"   토큰 타입: {data.get('token_type', 'N/A')}")
                print(f"   만료 시간: {data.get('expires_in', 'N/A')}초")
                print(f"   Access Token: {data.get('access_token', '')[:50]}...")
                return True
            else:
                print(f"❌ 토큰 발급 실패")
                print(f"   응답: {response.text}")
                return False
                
    except httpx.TimeoutException:
        print("❌ 요청 시간 초과")
        return False
    except httpx.ConnectError as e:
        print(f"❌ 연결 오류: {e}")
        print("   네트워크 연결을 확인하세요.")
        return False
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_kis_current_price():
    """현재가 조회 API 테스트 (토큰 발급 후)"""
    print("\n📊 현재가 조회 API 테스트 중...")
    
    if not settings.KIS_APP_KEY or not settings.KIS_APP_SECRET:
        print("❌ API 키가 설정되지 않았습니다.")
        return False
    
    try:
        # 먼저 토큰 발급
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                f"{settings.KIS_BASE_URL}/oauth2/tokenP",
                headers={"content-type": "application/json"},
                json={
                    "grant_type": "client_credentials",
                    "appkey": settings.KIS_APP_KEY,
                    "appsecret": settings.KIS_APP_SECRET
                },
                timeout=10.0
            )
            
            if token_response.status_code != 200:
                print(f"❌ 토큰 발급 실패: {token_response.text}")
                return False
            
            token_data = token_response.json()
            access_token = token_data.get("access_token")
            
            # 현재가 조회 (예: 삼성전자 005930)
            # 실제 API 엔드포인트는 KIS API 문서를 참조해야 합니다
            print("   주의: 실제 현재가 조회는 올바른 TR_ID와 엔드포인트가 필요합니다.")
            print("   여기서는 토큰 발급만 확인합니다.")
            
            return True
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False

async def main():
    """메인 함수"""
    print("=" * 60)
    print("한국투자증권 API 연결 테스트")
    print("=" * 60)
    print()
    
    # 토큰 발급 테스트
    token_success = await test_kis_token()
    
    if token_success:
        # 현재가 조회 테스트 (선택적)
        await test_kis_current_price()
    
    print()
    print("=" * 60)
    if token_success:
        print("✅ API 연결 테스트 완료!")
    else:
        print("❌ API 연결 테스트 실패")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())

