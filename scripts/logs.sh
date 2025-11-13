#!/bin/bash

# Docker Compose 로그 확인
cd "$(dirname "$0")/.."

SERVICE=${1:-""}

if [ -z "$SERVICE" ]; then
    echo "📝 전체 서비스 로그 확인 중..."
    docker-compose logs -f
else
    echo "📝 $SERVICE 서비스 로그 확인 중..."
    docker-compose logs -f "$SERVICE"
fi

