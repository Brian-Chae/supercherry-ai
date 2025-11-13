#!/bin/bash

# Docker Compose로 전체 스택 중지
cd "$(dirname "$0")/.."

echo "🛑 ETF 자동매매 시스템 중지 중..."

docker-compose down

echo "✅ 서비스가 중지되었습니다!"

