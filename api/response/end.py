from .message import Message


class End(Message):
    def json(self, **kwargs) -> dict[str, any]:
        return {
            "type": "end",
            **kwargs
        }
