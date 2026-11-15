from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from typing import Optional
from datetime import datetime, timezone
import json
from app.core.websocket import ws_manager
from app.repositories.estado_repository import EstadoRepository
from app.repositories.admin_repository import admin_repo
from app.core.security import decode_access_token, verify_vehicle_access

router = APIRouter(tags=["WebSocket"])
estado_repo = EstadoRepository()

@router.websocket("/ws/vehiculos/{id_vehiculo}")
async def websocket_vehiculo(websocket: WebSocket, id_vehiculo: int, token: Optional[str] = None):
    """
    Endpoint WebSocket autenticado para monitoreo y recepción de telemetría en tiempo real.
    Si se proporciona token JWT, valida pertenencia y derechos de suscripción al canal.
    """
    if token:
        try:
            payload = decode_access_token(token)
            uid = payload.get("sub")
            user = None
            if uid:
                user = admin_repo.obtener_usuario_por_email(payload.get("email"))
            if not user:
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                return
            # Validar autorización sobre el canal del vehículo
            verify_vehicle_access(id_vehiculo, user, write_access=False)
        except Exception:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

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
            await websocket.receive_text()
    except (WebSocketDisconnect, Exception):
        ws_manager.disconnect(id_vehiculo, websocket)
