"""
Todo Manager 테스트

TDD Red 에이전트가 각 기능에 대한 테스트를 이 파일에 추가합니다.
8교시부터 시작합니다.
"""
import pytest
from todo.manager import TodoManager
from todo.models import Status


class TestTodoManager:
    """TodoManager 단위 테스트"""

    def setup_method(self):
        """각 테스트 전 실행: 새 TodoManager 인스턴스 생성"""
        self.manager = TodoManager()

    def test_add_빈문자열_입력시_ValueError_발생(self):
        # Arrange
        empty_title = ""

        # Act & Assert
        with pytest.raises(ValueError):
            self.manager.add(empty_title)

    def test_complete_존재하는_id로_완료처리시_status가_DONE으로_변경(self):
        # Arrange
        todo = self.manager.add("할일 항목")

        # Act
        result = self.manager.complete(todo.id)

        # Assert
        assert result.status == Status.DONE

    def test_complete_존재하지않는_id로_완료처리시_ValueError_발생(self):
        # Arrange
        존재하지_않는_id = 999

        # Act & Assert
        with pytest.raises(ValueError):
            self.manager.complete(존재하지_않는_id)

    def test_list_by_status_pending_필터시_미완료_항목만_반환(self):
        # Arrange
        todo1 = self.manager.add("미완료 항목")
        todo2 = self.manager.add("완료할 항목")
        self.manager.complete(todo2.id)

        # Act
        result = self.manager.list_by_status(Status.PENDING)

        # Assert
        assert len(result) == 1
        assert result[0].id == todo1.id

    def test_list_by_status_done_필터시_완료_항목만_반환(self):
        # Arrange
        todo1 = self.manager.add("미완료 항목")
        todo2 = self.manager.add("완료할 항목")
        self.manager.complete(todo2.id)

        # Act
        result = self.manager.list_by_status(Status.DONE)

        # Assert
        assert len(result) == 1
        assert result[0].id == todo2.id

    def test_list_by_status_전체가_pending일때_done_필터시_빈_리스트_반환(self):
        # Arrange
        self.manager.add("미완료 항목")

        # Act
        result = self.manager.list_by_status(Status.DONE)

        # Assert
        assert result == []
