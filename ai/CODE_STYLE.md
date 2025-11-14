# 코드 스타일 가이드

## Python (Backend)

### 포맷팅

- **Black**: 코드 포맷터 (줄 길이 88자)
- **isort**: import 정렬
- **flake8**: 린터

### 설정

```bash
# Black 설정 (pyproject.toml)
[tool.black]
line-length = 88
target-version = ['py311']

# isort 설정 (pyproject.toml)
[tool.isort]
profile = "black"
line_length = 88
```

### 네이밍 컨벤션

- **변수/함수**: `snake_case`
- **클래스**: `PascalCase`
- **상수**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`

### 예시

```python
# 좋은 예시
def get_user_balance(user_id: int) -> float:
    """사용자 잔고를 조회합니다."""
    pass

class KISAPIClient:
    BASE_URL = "https://api.example.com"
    
    def _get_token(self) -> str:
        """내부 메서드"""
        pass

# 나쁜 예시
def getUserBalance(userId):  # camelCase 사용
    pass

def get_user_balance(user_id):  # 타입 힌트 없음
    pass
```

### 타입 힌트

- 모든 함수에 타입 힌트 사용
- 복잡한 타입은 `typing` 모듈 사용

```python
from typing import Optional, List, Dict, Any

def process_orders(
    orders: List[Dict[str, Any]],
    limit: Optional[int] = None
) -> List[Order]:
    pass
```

### Docstring

- Google 스타일 사용

```python
def calculate_vwap(prices: List[float], volumes: List[int]) -> float:
    """VWAP를 계산합니다.
    
    Args:
        prices: 가격 리스트
        volumes: 거래량 리스트
    
    Returns:
        계산된 VWAP 값
    
    Raises:
        ValueError: prices와 volumes의 길이가 다를 때
    """
    if len(prices) != len(volumes):
        raise ValueError("Prices and volumes must have the same length")
    # ...
```

## JavaScript/TypeScript (Frontend)

### 포맷팅

- **Prettier**: 코드 포맷터
- **ESLint**: 린터

### 설정

```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

### 네이밍 컨벤션

- **변수/함수**: `camelCase`
- **컴포넌트**: `PascalCase`
- **상수**: `UPPER_SNAKE_CASE`
- **Private**: `_leadingUnderscore`

### 예시

```javascript
// 좋은 예시
const API_BASE_URL = 'http://localhost:8000';

function getUserBalance(userId) {
  // ...
}

const OrderList = () => {
  // ...
};

// 나쁜 예시
const api_base_url = 'http://localhost:8000';  // snake_case
function GetUserBalance() {  // PascalCase (함수는 camelCase)
  // ...
}
```

### 컴포넌트 구조

```jsx
// 1. Import
import React, { useState, useEffect } from 'react';
import api from '../services/api';

// 2. Component 정의
const OrderList = () => {
  // 3. State
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);

  // 4. Effects
  useEffect(() => {
    loadOrders();
  }, []);

  // 5. Handlers
  const handleLoad = async () => {
    // ...
  };

  // 6. Render
  return (
    <div>
      {/* ... */}
    </div>
  );
};

// 7. Export
export default OrderList;
```

## 공통 규칙

### 주석

- **Why**를 설명 (What은 코드로)
- 복잡한 로직에만 주석 추가
- TODO 주석은 이슈로 변환

```python
# 좋은 예시
# KIS API는 1분당 1회 토큰 발급 제한이 있어서
# 기존 토큰을 재사용합니다
if token.is_valid():
    return token

# 나쁜 예시
# 변수에 값을 할당
value = 10
```

### 에러 처리

- 명확한 에러 메시지
- 적절한 예외 타입 사용
- 로깅 추가

```python
# 좋은 예시
try:
    result = api_client.get_balance(account_id)
except KISAPIError as e:
    logger.error(f"KIS API error: {e}")
    raise HTTPException(
        status_code=500,
        detail=f"Failed to get balance: {str(e)}"
    )
```

### 함수 크기

- 함수는 하나의 일만 수행
- 20-30줄 이내 권장
- 복잡한 로직은 작은 함수로 분리

### 중복 코드

- DRY (Don't Repeat Yourself) 원칙
- 공통 로직은 함수/유틸리티로 추출
- 코드 재사용성 고려

## 파일 구조

### Backend

```
backend/
├── app/
│   ├── api/          # API 엔드포인트
│   ├── models/       # 데이터베이스 모델
│   ├── schemas/      # Pydantic 스키마
│   ├── services/     # 비즈니스 로직
│   └── utils/        # 유틸리티 함수
```

### Frontend

```
frontend/
├── src/
│   ├── components/   # 재사용 가능한 컴포넌트
│   ├── pages/        # 페이지 컴포넌트
│   ├── services/     # API 서비스
│   ├── context/      # React Context
│   └── hooks/        # Custom Hooks
```

## 코드 리뷰 체크리스트

- [ ] 네이밍이 명확한가?
- [ ] 함수가 하나의 일만 하는가?
- [ ] 중복 코드가 없는가?
- [ ] 에러 처리가 적절한가?
- [ ] 타입 힌트가 있는가?
- [ ] 주석이 필요한가?
- [ ] 테스트가 있는가?

