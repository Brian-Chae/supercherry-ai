# 멀티 스테이지 빌드
FROM python:3.11-slim as builder

# Poetry 설치
RUN pip install poetry==1.8.3

# 작업 디렉토리 설정
WORKDIR /app

# Poetry 설정 (가상환경 비활성화 - 시스템 Python 사용)
RUN poetry config virtualenvs.create false

# 의존성 파일 복사
COPY pyproject.toml ./
COPY poetry.lock* ./

# 의존성 설치
RUN poetry install --no-interaction --no-ansi --no-root || \
    (poetry lock --no-update && poetry install --no-interaction --no-ansi --no-root)

# 프로덕션 스테이지
FROM python:3.11-slim

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# builder 스테이지에서 Python 패키지 복사
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 애플리케이션 코드 복사
COPY . .

# 포트 노출
EXPOSE 8000

# 헬스체크
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# 서버 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

