# Todo Manager - 아키텍처 문서 (통합 실습 완성본)

## 디렉터리 구조

```
AN.1.1/
├── src/
│   └── todo/
│       ├── __init__.py
│       ├── models.py      # Todo, Status
│       └── manager.py     # TodoManager
├── tests/
│   └── test_manager.py
└── pyproject.toml
```

## 핵심 클래스

### `TodoManager` 공개 인터페이스

| 메서드 | 시그니처 | 설명 |
|--------|----------|------|
| `add` | `(title: str) -> Todo` | 새 항목 추가 |
| `list_all` | `() -> list[Todo]` | 전체 목록 |
| `list_by_status` | `(status: Status) -> list[Todo]` | 상태별 필터링 |
| `complete` | `(todo_id: int) -> Todo` | 완료 처리 |
| `delete` | `(todo_id: int) -> None` | 삭제 |
