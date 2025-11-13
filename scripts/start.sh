#!/bin/bash

# Docker Compose로 전체 스택 실행
cd "$(dirname "$0")/.."

echo "🚀 ETF 자동매매 시스템 시작 중..."

# .env 파일 확인
if [ ! -f .env ]; then
    echo "⚠️  .env 파일이 없습니다. .env.example을 복사하여 생성하세요."
    echo "   cp .env.example .env"
    exit 1
fi

# Docker Compose 실행
docker-compose up -d

echo "✅ 서비스가 시작되었습니다!"
echo ""
echo "📊 서비스 상태 확인:"
docker-compose ps
echo ""
echo "📝 로그 확인:"
echo "   docker-compose logs -f [service_name]"
echo ""
echo "🌐 접속 URL:"
echo "   프론트엔드: http://localhost:5173"
echo "   백엔드 API: http://localhost:8000"
echo "   API 문서: http://localhost:8000/docs"
echo "   데이터베이스: localhost:5432"

