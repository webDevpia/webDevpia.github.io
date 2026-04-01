---
description: "Use when writing, reviewing, or modifying Python code for Todo Manager. Enforces naming, type hints, and function design rules."
applyTo: "**/*.py"
---

# Todo Manager 파이썬 코딩 지침

## 언어 규칙

- 변수명, 함수명, 클래스명은 영어로 작성한다.
- 함수명과 변수명은 snake_case, 클래스명은 PascalCase를 사용한다.
- 코드 주석과 docstring은 한국어로 작성한다.

## 타입 힌트

- 모든 함수 시그니처에 타입 힌트를 포함한다.
- 반환 타입도 반드시 명시한다 (`-> None` 포함).

## 함수 설계

- 함수는 단일 책임 원칙을 따른다.
- 중첩 깊이는 3 이하로 유지한다.
- 모든 공개 메서드에 한국어 docstring을 작성한다.
