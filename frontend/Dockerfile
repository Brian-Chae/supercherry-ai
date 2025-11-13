# 개발 모드용 Dockerfile
FROM node:20-alpine

WORKDIR /app

# 패키지 파일 복사
COPY package.json yarn.lock ./

# 의존성 설치
RUN yarn install --frozen-lockfile

# 소스 코드 복사
COPY . .

# 포트 노출
EXPOSE 5173

# 개발 서버 실행
CMD ["yarn", "dev", "--host", "0.0.0.0"]

