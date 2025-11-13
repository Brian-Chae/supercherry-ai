#!/bin/bash

# 개발 모드: 데이터베이스만 Docker로 실행
cd "$(dirname "$0")/.."

echo "🚀 개발 모드: 데이터베이스만 시작 중..."

# .env 파일 확인
if [ ! -f .env ]; then
    echo "⚠️  .env 파일이 없습니다. .env.example을 복사하여 생성하세요."
    echo "   cp .env.example .env"
    exit 1
fi

# 데이터베이스만 시작
docker-compose -f docker-compose.dev.yml up -d db

echo "✅ 데이터베이스가 시작되었습니다!"
echo ""
echo "📊 서비스 상태 확인:"
docker-compose -f docker-compose.dev.yml ps
echo ""
echo "📝 로그 확인:"
echo "   docker-compose -f docker-compose.dev.yml logs -f db"
echo ""
echo "💡 백엔드와 프론트엔드는 로컬에서 실행하세요:"
echo "   백엔드: cd backend && poetry run uvicorn app.main:app --reload"
echo "   프론트엔드: cd frontend && yarn dev"
echo ""
echo "🗄️  데이터베이스: localhost:5432"

