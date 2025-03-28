from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    """
    Represents a message in a chat conversation.

    Attributes:
        role: The role of the message sender ('user' or 'assistant').
        content: The content of the message.
        timestamp: The timestamp of the message.
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


@dataclass
class Location:
    """
    Represents a location of a library branch.

    Attributes:
        branch: The name of the library branch.
        address: The address of the library branch.
    """

    branch: str
    address: str

    def to_dict(self) -> dict[str, str]:
        """
        Returns a dictionary representation of the location.

        Returns:
            dict[str, str]: A dictionary containing the branch name and address.
        """
        return {"branch": self.branch, "address": self.address}
