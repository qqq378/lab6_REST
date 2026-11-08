import threading
from typing import Dict, List, Optional
from app.models import AuditCreate


class AuditStore:
    def __init__(self) -> None:
        self._data: Dict[int, dict] = {}
        self._next_id: int = 1
        self._lock = threading.Lock()

    def list(self) -> List[dict]:
        with self._lock:
            return list(self._data.values())

    def get(self, audit_id: int) -> Optional[dict]:
        with self._lock:
            return self._data.get(audit_id)

    def create(self, payload: AuditCreate) -> dict:
        with self._lock:
            record = payload.model_dump()
            record["id"] = self._next_id
            self._data[self._next_id] = record
            self._next_id += 1
            return record

    def delete(self, audit_id: int) -> bool:
        with self._lock:
            if audit_id in self._data:
                del self._data[audit_id]
                return True
            return False

    def clear(self) -> None:
        with self._lock:
            self._data.clear()
            self._next_id = 1


audit_store = AuditStore()