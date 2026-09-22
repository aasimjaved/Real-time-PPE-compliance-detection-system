from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:
    """Tracks active WebSocket clients per camera_id so we can broadcast
    annotated frames / violation events to every dashboard watching that feed."""

    def __init__(self):
        self.active: Dict[str, List[WebSocket]] = {}

    async def connect(self, camera_id: str, ws: WebSocket):
        await ws.accept()
        self.active.setdefault(camera_id, []).append(ws)

    def disconnect(self, camera_id: str, ws: WebSocket):
        if camera_id in self.active and ws in self.active[camera_id]:
            self.active[camera_id].remove(ws)
            if not self.active[camera_id]:
                del self.active[camera_id]

    async def broadcast(self, camera_id: str, message: dict):
        dead = []
        for ws in self.active.get(camera_id, []):
            try:
                await ws.send_json(message)
            except Exception:  # noqa: BLE001
                dead.append(ws)
        for ws in dead:
            self.disconnect(camera_id, ws)


manager = ConnectionManager()
