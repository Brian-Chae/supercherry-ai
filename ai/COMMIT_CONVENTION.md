# 커밋 메시지 컨벤션

## Conventional Commits 규칙

이 프로젝트는 [Conventional Commits](https://www.conventionalcommits.org/) 스펙을 따릅니다.

## 기본 형식

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Type (필수)

- **feat**: 새로운 기능 추가
- **fix**: 버그 수정
- **docs**: 문서 수정
- **style**: 코드 포맷팅, 세미콜론 누락 등 (코드 변경 없음)
- **refactor**: 코드 리팩토링
- **test**: 테스트 코드 추가/수정
- **chore**: 빌드 업무 수정, 패키지 매니저 설정 등
- **perf**: 성능 개선
- **ci**: CI/CD 설정 변경
- **build**: 빌드 시스템 또는 외부 의존성 변경

## Scope (선택)

변경이 발생한 영역을 명시합니다.

- `backend`: 백엔드 관련
- `frontend`: 프론트엔드 관련
- `api`: API 관련
- `auth`: 인증 관련
- `db`: 데이터베이스 관련
- `kis`: 한국투자증권 API 관련
- `ui`: UI/UX 관련
- `config`: 설정 파일 관련

## Subject (필수)

- 50자 이내로 작성
- 첫 글자는 대문자로 시작하지 않음
- 마지막에 마침표(.) 사용하지 않음
- 명령형으로 작성 (예: "추가" 대신 "add")

## Body (선택)

- 72자마다 줄바꿈
- 무엇을, 왜 변경했는지 설명
- 어떻게 변경했는지는 코드로 설명되므로 생략 가능

## Footer (선택)

- 이슈 번호 참조: `Closes #123`, `Fixes #456`
- Breaking Changes: `BREAKING CHANGE: 설명`

## 예시

### 좋은 예시

```bash
feat(api): add order history endpoint

Add GET /api/order endpoint to retrieve user's order history
with pagination support.

Closes #123
```

```bash
fix(kis): resolve datetime timezone comparison error

Replace datetime.utcnow() with datetime.now(timezone.utc)
to fix comparison error between timezone-aware and naive datetimes.

Fixes #456
```

```bash
docs: update README with KIS API setup instructions
```

```bash
refactor(backend): extract KIS API client to separate service

Move KIS API client logic from api/market.py to services/kis_api.py
for better code organization and reusability.
```

### 나쁜 예시

```bash
# 너무 짧고 모호함
fix: bug

# 타입이 명확하지 않음
update: something

# 과도하게 길고 불필요한 정보
feat: add a new feature that allows users to view their order history in the dashboard page with pagination and filtering options which was requested by the product team last week
```

## 커밋 작성 체크리스트

- [ ] Type이 명확한가?
- [ ] Scope가 적절한가?
- [ ] Subject가 50자 이내인가?
- [ ] 명령형으로 작성되었는가?
- [ ] 관련 이슈 번호를 참조했는가?
- [ ] Breaking Changes가 있다면 명시했는가?

## 커밋 빈도

- 논리적으로 관련된 변경사항은 하나의 커밋으로 묶기
- 작은 단위로 자주 커밋하기
- 한 커밋에 여러 기능을 섞지 않기

## 커밋 전 체크리스트

- [ ] 코드가 정상적으로 작동하는가?
- [ ] 테스트가 통과하는가?
- [ ] 린터 오류가 없는가?
- [ ] 불필요한 주석이나 디버그 코드가 없는가?
- [ ] .env 파일 등 민감한 정보가 포함되지 않았는가?

