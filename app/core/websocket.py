from fastapi import WebSocket
from typing import Dict, List
import json

class WebSocketConnectionManager:
    """Clase POO para gestionar conexiones WebSocket en tiempo real por vehículo."""
    
    def __init__(self):
        # Mapea id_vehiculo -> lista de WebSockets conectados
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, vehiculo_id: int, websocket: WebSocket):
        await websocket.accept()
        if vehiculo_id not in self.active_connections:
            self.active_connections[vehiculo_id] = []
        self.active_connections[vehiculo_id].append(websocket)

    def disconnect(self, vehiculo_id: int, websocket: WebSocket):
        if vehiculo_id in self.active_connections:
            if websocket in self.active_connections[vehiculo_id]:
                self.active_connections[vehiculo_id].remove(websocket)
            if not self.active_connections[vehiculo_id]:
                del self.active_connections[vehiculo_id]

    async def broadcast_to_vehicle(self, vehiculo_id: int, message: dict):
        """Envía el evento JSON únicamente a los clientes que monitorean ese vehículo."""
        if vehiculo_id in self.active_connections:
            payload = json.dumps(message, default=str)
            for connection in self.active_connections[vehiculo_id]:
                try:
                    await connection.send_text(payload)
                except Exception:
                    pass

ws_manager = WebSocketConnectionManager()
