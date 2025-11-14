# 릴리스 프로세스

## 버전 관리 규칙

이 프로젝트는 [Semantic Versioning](https://semver.org/)을 따릅니다.

### 형식: MAJOR.MINOR.PATCH

- **MAJOR**: 호환되지 않는 API 변경
- **MINOR**: 하위 호환성을 유지하는 기능 추가
- **PATCH**: 하위 호환성을 유지하는 버그 수정

### 예시

- `1.0.0` → `1.0.1`: 버그 수정
- `1.0.1` → `1.1.0`: 새로운 기능 추가
- `1.1.0` → `2.0.0`: Breaking Changes

## 릴리스 프로세스

### 1. Release 브랜치 생성

```bash
# Develop 브랜치에서 최신 코드 가져오기
git checkout develop
git pull origin develop

# Release 브랜치 생성
git checkout -b release/v1.0.0
git push origin release/v1.0.0
```

### 2. 릴리스 준비

#### 버전 번호 업데이트

- `backend/pyproject.toml`: `version = "1.0.0"`
- `frontend/package.json`: `"version": "1.0.0"`
- `README.md`: 버전 정보 업데이트

#### 체크리스트

- [ ] 모든 기능이 develop에 병합되었는가?
- [ ] 테스트가 모두 통과하는가?
- [ ] 문서가 최신 상태인가?
- [ ] CHANGELOG.md 업데이트
- [ ] Breaking Changes 문서화

### 3. 릴리스 테스트

```bash
# 로컬에서 전체 테스트 실행
cd backend && poetry run pytest
cd frontend && yarn test

# 통합 테스트
docker-compose up --build
# 수동 테스트 수행
```

### 4. Main 브랜치로 병합

```bash
# Release 브랜치를 Main으로 병합
git checkout main
git pull origin main
git merge release/v1.0.0 --no-ff

# 태그 생성
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main --tags
```

### 5. Develop 브랜치에 병합

```bash
# Release 브랜치를 Develop에도 병합
git checkout develop
git merge release/v1.0.0 --no-ff
git push origin develop
```

### 6. Release 브랜치 삭제

```bash
git branch -d release/v1.0.0
git push origin --delete release/v1.0.0
```

### 7. GitHub Release 생성

1. GitHub 저장소의 Releases 페이지 접속
2. "Draft a new release" 클릭
3. 태그 선택: `v1.0.0`
4. 제목: `Release v1.0.0`
5. 설명: CHANGELOG.md 내용 복사
6. "Publish release" 클릭

## Hotfix 프로세스

프로덕션 환경의 긴급 버그 수정:

### 1. Hotfix 브랜치 생성

```bash
git checkout main
git pull origin main
git checkout -b hotfix/fix-critical-bug
```

### 2. 버그 수정 및 테스트

```bash
# 버그 수정
# 테스트 작성 및 실행
```

### 3. Main 브랜치로 병합

```bash
git checkout main
git merge hotfix/fix-critical-bug --no-ff
git tag -a v1.0.1 -m "Hotfix: Critical bug fix"
git push origin main --tags
```

### 4. Develop 브랜치에 병합

```bash
git checkout develop
git merge hotfix/fix-critical-bug --no-ff
git push origin develop
```

### 5. Hotfix 브랜치 삭제

```bash
git branch -d hotfix/fix-critical-bug
git push origin --delete hotfix/fix-critical-bug
```

## CHANGELOG.md 관리

### 형식

```markdown
# Changelog

## [1.0.0] - 2025-11-13

### Added
- 사용자 인증 시스템 (JWT)
- 한국투자증권 API 연동
- 현재가 조회 기능
- 주문 기능 (매수/매도)
- 잔고 조회 기능

### Changed
- API 응답 형식 개선

### Fixed
- datetime timezone 비교 오류 수정

### Security
- 민감한 정보 환경 변수로 분리
```

### 작성 규칙

- 날짜 형식: YYYY-MM-DD
- 카테고리: Added, Changed, Deprecated, Removed, Fixed, Security
- 각 항목은 간결하고 명확하게 작성
- 사용자 관점에서 작성

## 배포 체크리스트

### 배포 전

- [ ] 모든 테스트 통과
- [ ] 코드 리뷰 완료
- [ ] 문서 업데이트 완료
- [ ] 환경 변수 설정 확인
- [ ] 데이터베이스 마이그레이션 준비
- [ ] 백업 계획 수립

### 배포 중

- [ ] 데이터베이스 백업
- [ ] 마이그레이션 실행
- [ ] 서비스 재시작
- [ ] 헬스 체크 확인

### 배포 후

- [ ] 모니터링 확인
- [ ] 로그 확인
- [ ] 사용자 피드백 수집
- [ ] 롤백 계획 준비

## 롤백 프로세스

문제 발생 시 즉시 롤백:

```bash
# 이전 버전 태그 확인
git tag -l

# 이전 버전으로 체크아웃
git checkout v1.0.0

# 롤백 배포
# (배포 스크립트 실행)
```

