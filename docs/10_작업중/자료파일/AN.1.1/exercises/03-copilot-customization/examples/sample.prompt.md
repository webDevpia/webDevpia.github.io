---
description: "Todo Manager 프로젝트에 새 기능과 테스트를 함께 추가할 때 사용합니다."
name: "New Feature"
agent: "agent"
---

다음 기능을 Todo Manager 프로젝트에 추가해주세요.

기능명: ${input:featureName:구현할 기능명을 입력하세요}

요구사항:
${input:requirements:기능 요구사항을 입력하세요}

다음 내용을 포함해주세요:
1. `src/todo/manager.py` 에 메서드 추가
2. `tests/test_manager.py` 에 테스트 추가 (준비-실행-검증, Arrange-Act-Assert 패턴)
3. 모든 기존 테스트가 계속 통과하는지 확인
