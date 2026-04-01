from .models import Todo, Status


class TodoManager:
    """Todo 항목을 관리하는 클래스"""

    def __init__(self) -> None:
        self._todos: list[Todo] = []
        self._next_id: int = 1

    def add(self, title: str) -> Todo:
        """새 Todo를 추가하고 반환한다"""
        if not title:
            raise ValueError("title은 빈 문자열일 수 없습니다.")
        todo = Todo(id=self._next_id, title=title)
        self._todos.append(todo)
        self._next_id += 1
        return todo

    def list_all(self) -> list[Todo]:
        """전체 Todo 목록을 반환한다"""
        raise NotImplementedError

    def complete(self, todo_id: int) -> Todo:
        """지정한 Todo를 완료 처리하고 반환한다"""
        todo = self._find_by_id(todo_id)
        todo.status = Status.DONE
        return todo

    def _find_by_id(self, todo_id: int) -> Todo:
        """ID에 해당하는 Todo를 찾아 반환한다"""
        for todo in self._todos:
            if todo.id == todo_id:
                return todo
        raise ValueError("존재하지 않는 ID입니다.")

    def list_by_status(self, status: Status) -> list[Todo]:
        """지정한 상태에 해당하는 Todo 목록을 반환한다"""
        return [todo for todo in self._todos if todo.status == status]

    def delete(self, todo_id: int) -> None:
        """지정한 Todo를 삭제한다"""
        raise NotImplementedError
