---
description: "테스트 작성, 리뷰, 수정 시 사용한다. pytest 규칙, AAA(Arrange-Act-Assert) 패턴, 테스트 네이밍 규칙을 포함한다."
applyTo: "tests/**"
---

# Todo Manager 테스트 작성 지침

## 테스트 프레임워크

- pytest를 사용한다.

## 테스트 명명 규칙

- 테스트 함수명은 `test_` 로 시작한다.
- 이름은 `test_메서드명_조건_기대결과` 형식을 권장한다.
  - 예: `test_add_제목이_빈_문자열_일_때_ValueError_발생`

## 테스트 구조

- Arrange-Act-Assert 패턴을 따른다.
- 한 테스트 함수는 한 가지 동작만 검증한다.
- 각 단계를 `# Arrange`, `# Act`, `# Assert` 주석으로 구분한다.
