#!/bin/bash

# 개발 모드: 데이터베이스만 중지
cd "$(dirname "$0")/.."

echo "🛑 개발 모드: 데이터베이스 중지 중..."

docker-compose -f docker-compose.dev.yml down

echo "✅ 데이터베이스가 중지되었습니다!"

