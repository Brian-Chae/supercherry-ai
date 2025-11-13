#!/bin/bash

# 테스트 사용자 생성 스크립트
cd "$(dirname "$0")/.."

echo "👤 테스트 사용자 생성 중..."

# 백엔드 디렉토리로 이동하여 실행
cd backend

# Poetry 환경에서 실행
if command -v poetry &> /dev/null; then
    poetry run python ../scripts/create-test-user.py
else
    # Poetry가 없으면 시스템 Python 사용
    python3 ../scripts/create-test-user.py
fi

