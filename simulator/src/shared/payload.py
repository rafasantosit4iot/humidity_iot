import time
import json

from shared.enum.scalar import Scalar

class Payload:
    def __init__(
        self,
        scalar: Scalar,
        id: str,
        value: int
    ):
        self.scalar = scalar
        self.id = id
        self.value = value

    def _generate_payload(self) -> str:
        payload = json.dumps(
            {
                self.scalar.value: self.value,
                "id": self.id,
                "timestamp": int(time.time())
            }
        )
        return payload 
        
    def get_payload(self)->str:
        payload = self._generate_payload()
        return payload