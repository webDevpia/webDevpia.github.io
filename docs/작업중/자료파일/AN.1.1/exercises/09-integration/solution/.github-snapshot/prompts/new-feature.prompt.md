---
description: "Todo Manager에 새 기능을 구현하고 테스트를 추가할 때 사용"
name: "New Feature"
agent: "agent"
---

다음 기능을 Todo Manager에 추가해주세요.

기능명: ${input:featureName:구현할 기능명을 입력하세요}

요구사항:
${input:requirements:기능 요구사항을 입력하세요}

다음을 포함해주세요:
1. `src/todo/manager.py` 에 메서드 추가 (한국어 docstring 포함)
2. `tests/test_manager.py` 에 테스트 추가 (Arrange-Act-Assert 패턴)
3. 모든 기존 테스트가 계속 통과하는지 확인
4. 프로젝트 코딩 지침 준수
