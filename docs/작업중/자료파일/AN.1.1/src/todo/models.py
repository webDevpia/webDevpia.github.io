from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Status(Enum):
    PENDING = "pending"
    DONE = "done"


@dataclass
class Todo:
    id: int
    title: str
    status: Status = Status.PENDING
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        mark = "✓" if self.status == Status.DONE else "○"
        return f"[{mark}] ({self.id}) {self.title}"
