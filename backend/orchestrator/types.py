from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    """
    A message class.
    """

    role: str
    content: str
    timestamp: datetime

    def __str__(self) -> str:
        return (
            f"{self.role} @ {self.timestamp.strftime('%I:%M:%S %p')} : {self.content}"
        )

    def __repr__(self) -> str:
        return self.__str__()
