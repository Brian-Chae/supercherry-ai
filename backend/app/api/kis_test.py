"""
KIS API 연결 테스트 엔드포인트
"""
from fastapi import APIRouter, HTTPException, status
from app.config import settings
import httpx

router = APIRouter(prefix="/api/kis-test", tags=["kis-test"])


@router.get("/token")
async def test_kis_token():
    """KIS API 토큰 발급 테스트"""
    if not settings.KIS_APP_KEY or not settings.KIS_APP_SECRET:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="KIS_APP_KEY 또는 KIS_APP_SECRET이 설정되지 않았습니다."
        )
    
    try:
        async with httpx.AsyncClient() as client:
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
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "message": "토큰 발급 성공",
                    "token_type": data.get("token_type"),
                    "expires_in": data.get("expires_in"),
                    "access_token_preview": data.get("access_token", "")[:50] + "..."
                }
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error_code": error_data.get("error_code"),
                    "error_description": error_data.get("error_description", response.text)
                }
                
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="KIS API 요청 시간 초과"
        )
    except httpx.ConnectError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="KIS API 서버에 연결할 수 없습니다"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"오류 발생: {str(e)}"
        )

