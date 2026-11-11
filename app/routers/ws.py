from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from datetime import datetime, timezone
import json
from app.core.websocket import ws_manager
from app.repositories.estado_repository import EstadoRepository

router = APIRouter(tags=["WebSocket"])
estado_repo = EstadoRepository()

@router.websocket("/ws/vehiculos/{id_vehiculo}")
async def websocket_vehiculo(websocket: WebSocket, id_vehiculo: int):
    """
    Endpoint WebSocket para monitoreo y recepción de eventos de DEMO en tiempo real.
    Al conectarse, consulta RDS y emite el último estado disponible.
    """
    await ws_manager.connect(id_vehiculo, websocket)
    try:
        # Enviar estado inicial seguro con default=str para serializar fechas
        ultimo_estado = estado_repo.obtener_estado(id_vehiculo)
        payload = {
            "tipo": "CONEXION_ESTABLECIDA",
            "id_vehiculo": id_vehiculo,
            "estado_inicial": ultimo_estado,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await websocket.send_text(json.dumps(payload, default=str))
        
        while True:
            # Mantiene el socket escuchando sin cerrarse
            await websocket.receive_text()
    except (WebSocketDisconnect, Exception):
        ws_manager.disconnect(id_vehiculo, websocket)
