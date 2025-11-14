# Git 워크플로우 가이드

## 브랜치 전략

이 프로젝트는 **Git Flow** 기반의 브랜치 전략을 사용합니다.

### 주요 브랜치

- **`main`**: 프로덕션 환경에 배포되는 안정적인 코드
- **`develop`**: 다음 릴리스를 위한 개발 브랜치

### 보조 브랜치

- **`feature/*`**: 새로운 기능 개발
- **`hotfix/*`**: 프로덕션 버그 수정
- **`release/*`**: 릴리스 준비 및 테스트

## 브랜치 생성 규칙

### Feature 브랜치

```bash
# 기능 개발 시작
git checkout develop
git pull origin develop
git checkout -b feature/기능명

# 예시
git checkout -b feature/user-authentication
git checkout -b feature/kis-api-integration
```

**명명 규칙:**
- 소문자와 하이픈(-) 사용
- 명확하고 간결한 기능 설명
- 예: `feature/add-order-history`, `feature/improve-dashboard-ui`

### Hotfix 브랜치

```bash
# 긴급 버그 수정
git checkout main
git pull origin main
git checkout -b hotfix/버그설명

# 예시
git checkout -b hotfix/fix-login-error
git checkout -b hotfix/resolve-balance-api-timeout
```

### Release 브랜치

```bash
# 릴리스 준비
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0
```

## 브랜치 병합 규칙

### Feature → Develop

1. Feature 브랜치에서 작업 완료
2. Develop 브랜치에 최신 변경사항 반영
3. Pull Request 생성
4. 코드 리뷰 후 병합

```bash
# Feature 브랜치에서
git checkout feature/my-feature
git pull origin develop  # 최신 develop 반영
git push origin feature/my-feature

# GitHub에서 Pull Request 생성
# base: develop, compare: feature/my-feature
```

### Develop → Main (Release)

1. Release 브랜치 생성
2. 버전 번호 업데이트 및 테스트
3. Main 브랜치로 병합
4. 태그 생성

```bash
# Release 브랜치 생성
git checkout -b release/v1.0.0 develop

# 버전 업데이트, 테스트 후
git checkout main
git merge release/v1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main --tags
```

### Hotfix → Main & Develop

```bash
# Hotfix 완료 후
git checkout main
git merge hotfix/fix-bug
git tag -a v1.0.1 -m "Hotfix: 버그 수정"
git push origin main --tags

# Develop에도 병합
git checkout develop
git merge hotfix/fix-bug
git push origin develop
```

## 브랜치 삭제

병합 완료 후 브랜치 삭제:

```bash
# 로컬 브랜치 삭제
git branch -d feature/my-feature

# 원격 브랜치 삭제
git push origin --delete feature/my-feature
```

## 브랜치 보호 규칙

### Main 브랜치
- 직접 push 금지
- Pull Request 필수
- 최소 1명의 승인 필요
- CI/CD 통과 필수

### Develop 브랜치
- 직접 push 가능 (작은 수정사항)
- 주요 기능은 Pull Request 권장
- 코드 리뷰 권장
