# ETF 자동매매 시스템

한국투자증권 API를 이용한 ETF 자동매매 시스템입니다.

## 프로젝트 구조

```
supercherry_ai/
├── backend/          # FastAPI 백엔드
├── frontend/         # React 프론트엔드
├── scripts/          # 실행 스크립트
└── docker-compose.yml # Docker Compose 설정
```

## 기술 스택

### Backend
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT 인증
- 한국투자증권 Open API
- Poetry (의존성 관리)

### Frontend
- React
- React Router
- Tailwind CSS
- Recharts
- Axios
- Vite

## 개발 모드 실행 (권장)

개발 편의를 위해 데이터베이스만 Docker로 실행하고, 백엔드와 프론트엔드는 로컬에서 실행합니다.

### 1. 환경 변수 설정

```bash
# 루트 디렉토리의 .env 파일 확인/생성
cp .env.example .env  # 없으면 생성
# .env 파일을 편집하여 필요한 값 설정

# 백엔드 .env 파일도 동기화
cp .env backend/.env
```

**필수 환경 변수:**
- `KIS_APP_KEY`: 한국투자증권 API App Key
- `KIS_APP_SECRET`: 한국투자증권 API App Secret
- `DATABASE_URL`: PostgreSQL 연결 문자열
- `SECRET_KEY`: JWT 시크릿 키

### 2. 데이터베이스 시작

```bash
# 데이터베이스만 Docker로 실행
./scripts/dev-start.sh

# 또는 직접 실행
docker-compose -f docker-compose.dev.yml up -d
```

### 3. 백엔드 실행 (로컬)

```bash
cd backend
poetry install  # 처음 한 번만

# .env 파일 확인 (없으면 생성)
cp ../.env .env  # 또는 직접 생성

# 서버 실행 (0.0.0.0으로 실행하여 localhost 접근 가능)
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**중요**: `.env` 파일을 변경한 후에는 백엔드를 재시작해야 합니다.

### 4. 프론트엔드 실행 (로컬)

```bash
cd frontend
yarn install  # 처음 한 번만

# 환경 변수 설정 (없으면 생성)
cp .env.example .env
# .env 파일에 VITE_API_BASE_URL=http://localhost:8000 설정

# 개발 서버 실행
yarn dev
```

### 5. 접속

- **프론트엔드**: http://localhost:5173
- **백엔드 API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **KIS API 테스트**: http://localhost:8000/api/kis-test/token
- **데이터베이스**: localhost:5432

### 6. 테스트 사용자 생성 (선택)

```bash
# 기본 테스트 계정 생성
./scripts/create-test-user.sh

# 생성되는 계정 정보:
# 사용자명: testuser
# 비밀번호: test1234
# 이메일: test@example.com
```

### 7. KIS API 연결 테스트

```bash
# 스크립트로 테스트
cd backend
poetry run python ../scripts/test-kis-api-simple.py

# 또는 API 엔드포인트로 테스트
curl http://localhost:8000/api/kis-test/token
```

### 8. 데이터베이스 중지

```bash
./scripts/dev-stop.sh

# 또는
docker-compose -f docker-compose.dev.yml down
```

## 프로덕션 모드 실행 (전체 Docker)

프로덕션 환경이나 전체 스택을 Docker로 실행하려면:

```bash
# 전체 스택 시작
./scripts/start.sh

# 또는 직접 실행
docker-compose up -d
```

## Docker Compose 명령어

```bash
# 서비스 시작
docker-compose up -d

# 서비스 중지
docker-compose down

# 서비스 재시작
docker-compose restart [service_name]

# 로그 확인
docker-compose logs -f [service_name]

# 서비스 상태 확인
docker-compose ps

# 특정 서비스만 실행
docker-compose up backend db

# 빌드 재실행
docker-compose up --build
```

## 데이터베이스 마이그레이션

```bash
# 백엔드 컨테이너 접속
docker-compose exec backend bash

# Alembic 마이그레이션 실행
alembic upgrade head
```

## 환경 변수

### 백엔드 (.env)
- `DATABASE_URL`: PostgreSQL 연결 문자열
- `SECRET_KEY`: JWT 시크릿 키
- `KIS_APP_KEY`: 한국투자증권 API 키
- `KIS_APP_SECRET`: 한국투자증권 API 시크릿
- `CORS_ORIGINS`: 허용할 프론트엔드 URL

### 프론트엔드 (.env)
- `VITE_API_BASE_URL`: 백엔드 API URL

### 데이터베이스 (docker-compose.dev.yml)
- `POSTGRES_DB`: 데이터베이스 이름
- `POSTGRES_USER`: 사용자 이름
- `POSTGRES_PASSWORD`: 비밀번호

## 주요 기능

- 사용자 인증 (JWT)
- 한국투자증권 API 연동
- 현재가 조회
- 주문 (매수/매도)
- 잔고 조회
- 뉴스 조회
- VWAP 기반 자동매매 전략
- 전략 설정 및 관리

## 문제 해결

### 포트가 이미 사용 중인 경우
```bash
# 포트 사용 확인
lsof -i :8000
lsof -i :5173
lsof -i :5432

# docker-compose.yml에서 포트 변경
```

### 데이터베이스 연결 실패
```bash
# 데이터베이스 컨테이너 상태 확인
docker-compose -f docker-compose.dev.yml ps db

# 데이터베이스 로그 확인
docker-compose -f docker-compose.dev.yml logs db
```

### 백엔드가 .env 파일을 읽지 못하는 경우
```bash
# 백엔드 .env 파일 확인
cat backend/.env

# 루트 .env 파일을 백엔드로 복사
cp .env backend/.env

# 백엔드 재시작 (--reload 옵션이면 자동 재시작됨)
```

### 컨테이너 재빌드
```bash
docker-compose build --no-cache
docker-compose up -d
```

## 라이선스

MIT
