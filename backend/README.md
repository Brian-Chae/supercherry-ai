# ETF 자동매매 시스템 백엔드

한국투자증권 API를 이용한 ETF 자동매매 시스템의 백엔드 서버입니다.

## 설치 및 실행

### Poetry 사용 (권장)

```bash
# 의존성 설치
poetry install

# 서버 실행
poetry run uvicorn app.main:app --reload
```

### 기존 venv 사용

```bash
# 가상환경 활성화
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn app.main:app --reload
```

## 환경 변수

`.env` 파일을 생성하여 다음 변수들을 설정하세요:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/etf_trading
SECRET_KEY=your-secret-key-here
KIS_APP_KEY=your-app-key
KIS_APP_SECRET=your-app-secret
```

## API 문서

서버 실행 후 `http://localhost:8000/docs`에서 Swagger UI를 통해 API 문서를 확인할 수 있습니다.

