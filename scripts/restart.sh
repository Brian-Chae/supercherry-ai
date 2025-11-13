#!/bin/bash

# Docker Compose로 전체 스택 재시작
cd "$(dirname "$0")/.."

echo "🔄 ETF 자동매매 시스템 재시작 중..."

docker-compose restart

echo "✅ 서비스가 재시작되었습니다!"

