#!/usr/bin/env python3
"""
한국투자증권 API 간단한 연결 테스트
토큰 발급만 확인 (1분당 1회 제한 고려)
"""
import sys
import os
import asyncio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

import httpx
from app.config import settings

async def test_kis_token():
    """KIS API 토큰 발급 테스트"""
    print("🔐 한국투자증권 API 토큰 발급 테스트")
    print("=" * 60)
    
    if not settings.KIS_APP_KEY or not settings.KIS_APP_SECRET:
        print("❌ KIS_APP_KEY 또는 KIS_APP_SECRET이 설정되지 않았습니다.")
        return False
    
    print(f"✅ App Key: {settings.KIS_APP_KEY[:15]}...")
    print(f"✅ App Secret: {'설정됨' if settings.KIS_APP_SECRET else '없음'}")
    print(f"✅ Base URL: {settings.KIS_BASE_URL}")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            print("📡 토큰 발급 요청 중...")
            response = await client.post(
                f"{settings.KIS_BASE_URL}/oauth2/tokenP",
                headers={"content-type": "application/json"},
                json={
                    "grant_type": "client_credentials",
                    "appkey": settings.KIS_APP_KEY,
                    "appsecret": settings.KIS_APP_SECRET
                },
                timeout=10.0
            )
            
            print(f"   상태 코드: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 토큰 발급 성공!")
                print(f"   토큰 타입: {data.get('token_type', 'N/A')}")
                print(f"   만료 시간: {data.get('expires_in', 'N/A')}초 ({data.get('expires_in', 0) // 3600}시간)")
                print(f"   Access Token: {data.get('access_token', '')[:50]}...")
                print()
                print("💡 API 연결이 정상적으로 작동합니다!")
                return True
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                error_code = error_data.get('error_code', 'N/A')
                error_msg = error_data.get('error_description', response.text)
                
                print(f"❌ 토큰 발급 실패")
                print(f"   에러 코드: {error_code}")
                print(f"   에러 메시지: {error_msg}")
                
                if error_code == "EGW00133":
                    print()
                    print("⚠️  참고: 1분당 1회 제한으로 인한 오류입니다.")
                    print("   잠시 후 다시 시도하세요.")
                
                return False
                
    except httpx.TimeoutException:
        print("❌ 요청 시간 초과")
        return False
    except httpx.ConnectError as e:
        print(f"❌ 연결 오류: {e}")
        return False
    except Exception as e:
        print(f"❌ 오류 발생: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_kis_token())
    print()
    print("=" * 60)
    sys.exit(0 if success else 1)

