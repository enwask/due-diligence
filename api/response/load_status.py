from .message import Message


class LoadStatus(Message):
    def __init__(self, status: str):
        self.status = status

    def json(self, **kwargs) -> dict[str, any]:
        return {
            "type": "status",
            "message": self.status,
            **kwargs
        }
