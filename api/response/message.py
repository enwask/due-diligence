import json
from typing import Protocol


# Describes a message streamed as part of the comparison response
class Message(Protocol):
    def json(self, **kwargs) -> dict[str, any]: ...

    def str(self) -> str:
        return json.dumps(self.json())
