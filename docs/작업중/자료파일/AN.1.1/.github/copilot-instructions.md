# Todo Manager Workspace Guidelines

## Scope

- 이 파일은 워크스페이스 전역에 항상 적용되는 공통 지침이다.
- 파일별 세부 규칙은 `.github/instructions/*.instructions.md`에서 관리한다.

## Build And Test

- 의존성 설치: `uv sync`
- 전체 테스트 실행: `uv run pytest`
- 상세 테스트 실행: `uv run pytest -v`

## Project Structure

- 핵심 도메인 코드는 `src/todo/`에 위치한다.
- 테스트 코드는 `tests/`에 위치한다.
- 실습 템플릿과 해답은 `exercises/` 하위 폴더에 있으며, 필요할 때 참조한다.

## Working Conventions

- 변경은 요청 범위에 맞는 최소 단위로 수행한다.
- Python 코드를 수정할 때는 타입 힌트와 공개 메서드 docstring을 유지한다.
- 테스트 코드를 수정할 때는 `.github/instructions/testing.instructions.md` 규칙을 따른다.

## Documentation Rule

- 상세 설명은 `README.md`와 `exercises/*/README.md`를 우선 참조한다.
- 동일 내용을 이 파일에 중복으로 복사하지 않는다.

## 파일별 상세 지침

