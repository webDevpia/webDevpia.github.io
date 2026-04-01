---
description: "Use when writing, reviewing, or modifying pytest tests for Todo Manager. Enforces AAA pattern and test naming format."
applyTo: "tests/**"
---

# Todo Manager 테스트 작성 지침

## 테스트 프레임워크

- pytest를 사용한다.

## 테스트 명명 규칙

- 테스트 함수명은 `test_`로 시작한다.
- 테스트 함수명은 `test_메서드명_조건_기대결과` 형식으로 작성한다.
  - 예: `test_add_빈문자열_입력시_ValueError_발생`

## 테스트 구조

- 테스트는 Arrange-Act-Assert 패턴을 사용한다.
- 각 단계를 `# Arrange`, `# Act`, `# Assert` 주석으로 구분한다.
- 한 테스트 함수는 한 가지 동작만 검증한다.
