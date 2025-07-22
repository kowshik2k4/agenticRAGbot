from typing import Dict
import uuid

def create_message(sender: str, receiver: str, type_: str, payload: Dict) -> Dict:
    return {
        "sender": sender,
        "receiver": receiver,
        "type": type_,
        "trace_id": str(uuid.uuid4()),
        "payload": payload
    }

