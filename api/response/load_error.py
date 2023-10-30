from .message import Message


class LoadError(Message):
    def __init__(self, error: str):
        self.error = error

    def json(self, **kwargs) -> dict[str, any]:
        return {
            "type": "error",
            "error": self.error,
            **kwargs
        }
