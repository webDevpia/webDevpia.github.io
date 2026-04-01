# Todo Manager - 기여 가이드 (통합 실습 완성본)

## 코딩 컨벤션

- 변수명, 함수명, 클래스명은 영어 사용 (snake_case / PascalCase)
- 코드 주석과 docstring은 한국어 작성
- 모든 함수 시그니처에 타입 힌트 포함

## 테스트 규칙

- pytest 사용
- Arrange-Act-Assert 패턴
- 한 테스트 함수 = 한 가지 동작만 검증

## 개발 흐름

1. **Red**: 실패하는 테스트 작성 (TDD Red 에이전트)
2. **Green**: 최소 구현 (TDD Green 에이전트)
3. **Refactor**: 코드 개선 (TDD Refactor 에이전트)
