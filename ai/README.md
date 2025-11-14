# 코드 관리 가이드

이 디렉토리는 프로젝트의 코드 관리 및 협업 규칙을 담고 있습니다.

## 문서 목록

### 📋 [Git 워크플로우](./GIT_WORKFLOW.md)
브랜치 전략, 브랜치 생성/병합 규칙, 브랜치 보호 규칙 등 Git 사용 가이드

### 📝 [커밋 컨벤션](./COMMIT_CONVENTION.md)
커밋 메시지 작성 규칙, Conventional Commits 스펙 준수 가이드

### 👀 [코드 리뷰 가이드](./CODE_REVIEW_GUIDE.md)
Pull Request 작성 방법, 리뷰어/작성자 가이드라인, 승인 기준

### 🚀 [릴리스 프로세스](./RELEASE_PROCESS.md)
버전 관리 규칙, 릴리스 절차, Hotfix 프로세스, 배포 체크리스트

### 🎨 [코드 스타일 가이드](./CODE_STYLE.md)
Python/JavaScript 코드 스타일, 네이밍 컨벤션, 포맷팅 규칙

## 빠른 시작

### 1. 새 기능 개발

```bash
# Develop 브랜치에서 시작
git checkout develop
git pull origin develop

# Feature 브랜치 생성
git checkout -b feature/my-new-feature

# 작업 후 커밋
git add .
git commit -m "feat(api): add new endpoint"

# Push 및 PR 생성
git push origin feature/my-new-feature
```

### 2. 버그 수정

```bash
# Hotfix 브랜치 생성
git checkout main
git checkout -b hotfix/fix-bug-name

# 수정 후 커밋
git commit -m "fix(api): resolve bug description"

# Main과 Develop에 병합
```

### 3. 릴리스 준비

```bash
# Release 브랜치 생성
git checkout develop
git checkout -b release/v1.0.0

# 버전 업데이트, 테스트 후
# Main으로 병합 및 태그 생성
```

## 주요 규칙 요약

### 브랜치 전략
- `main`: 프로덕션 코드
- `develop`: 개발 브랜치
- `feature/*`: 기능 개발
- `hotfix/*`: 긴급 버그 수정
- `release/*`: 릴리스 준비

### 커밋 메시지
```
<type>(<scope>): <subject>

<body>

<footer>
```

### 코드 리뷰
- 모든 PR은 최소 1명의 승인 필요
- Main 브랜치는 직접 push 금지
- CI/CD 통과 필수

### 릴리스
- Semantic Versioning (MAJOR.MINOR.PATCH)
- Release 브랜치를 통한 릴리스
- 태그와 함께 배포

## 도구 및 설정

### 필수 도구

- **Git**: 버전 관리
- **Black** (Python): 코드 포맷터
- **Prettier** (JavaScript): 코드 포맷터
- **ESLint**: JavaScript 린터
- **pytest**: Python 테스트 프레임워크

### 권장 IDE 설정

- **VS Code**: Prettier, ESLint 확장 설치
- **PyCharm**: Black, isort 플러그인 설정

## 질문 및 제안

코드 관리 규칙에 대한 질문이나 개선 제안이 있으면 이슈를 생성해주세요.

## 참고 자료

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

