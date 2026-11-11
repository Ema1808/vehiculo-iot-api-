import asyncio
from datetime import datetime, timezone
from fastapi import HTTPException
from app.core.database import db_manager
from app.core.websocket import ws_manager
from app.repositories.vehiculo_repository import VehiculoRepository
from app.repositories.comando_repository import ComandoRepository
from app.repositories.estado_repository import EstadoRepository
from app.repositories.historial_repository import HistorialRepository
from app.repositories.demo_repository import DemoRepository

class VehicleService:
    def __init__(self):
        self.vehiculo_repo = VehiculoRepository()
        self.comando_repo = ComandoRepository()
        self.estado_repo = EstadoRepository()
        self.historial_repo = HistorialRepository()
        self.demo_repo = DemoRepository()
        self.demos_activas = set()
        self.cancelaciones = set()

    async def ejecutar_movimiento_individual(self, id_vehiculo: int, id_comando: int, origen: str):
        # 1. Validar que el vehículo exista y esté activo
        vehiculo = self.vehiculo_repo.obtener_por_id(id_vehiculo)
        if not vehiculo or not vehiculo.get("activo"):
            raise HTTPException(status_code=404, detail="Vehículo no encontrado o inactivo")

        # 2. Validar que el comando pertenezca a ese vehículo y esté activo
        comandos = self.comando_repo.obtener_por_vehiculo(id_vehiculo)
        comando_valido = next((c for c in comandos if c["id_comando"] == id_comando and c.get("activo", True)), None)
        if not comando_valido:
            raise HTTPException(status_code=400, detail="El comando no existe o no pertenece a este vehículo")

        # 3. Transacción atómica: Actualizar estado + Registrar en historial
        with db_manager.get_connection() as conn:
            try:
                self.estado_repo.actualizar_estado(id_vehiculo, id_comando, conectado=True, connection=conn)
                self.historial_repo.registrar(id_vehiculo, id_comando, origen, connection=conn)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise HTTPException(status_code=500, detail=f"Error en transacción: {str(e)}")

        # 4. Notificar vía WebSocket a los clientes conectados a este vehículo
        evento = {
            "tipo": "MOVIMIENTO_INDIVIDUAL",
            "id_vehiculo": id_vehiculo,
            "id_comando": id_comando,
            "comando": comando_valido["nombre"],
            "codigo": comando_valido["codigo"],
            "origen": origen,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await ws_manager.broadcast_to_vehicle(id_vehiculo, evento)
        return {"status": "success", "mensaje": "Movimiento registrado y notificado", "data": evento}

    async def iniciar_demo_async(self, id_vehiculo: int, id_demo: int):
        if id_vehiculo in self.demos_activas:
            raise HTTPException(status_code=409, detail="El vehículo ya tiene una DEMO en ejecución")

        vehiculo = self.vehiculo_repo.obtener_por_id(id_vehiculo)
        if not vehiculo:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        movimientos = self.demo_repo.obtener_movimientos(id_demo)
        if not movimientos:
            raise HTTPException(status_code=404, detail="La DEMO no existe o no tiene movimientos")

        asyncio.create_task(self._ejecutar_secuencia_demo(id_vehiculo, id_demo, movimientos))
        return {"status": "accepted", "mensaje": "Secuencia DEMO iniciada por WebSocket"}

    async def _ejecutar_secuencia_demo(self, id_vehiculo: int, id_demo: int, movimientos: list):
        self.demos_activas.add(id_vehiculo)
        self.cancelaciones.discard(id_vehiculo)

        try:
            # 1. Evento de inicio
            await ws_manager.broadcast_to_vehicle(id_vehiculo, {
                "tipo": "DEMO_INICIO",
                "id_vehiculo": id_vehiculo,
                "id_demo": id_demo,
                "total_movimientos": len(movimientos),
                "timestamp": datetime.now(timezone.utc).isoformat()
            })

            # 2. Procesar los N movimientos en orden
            for mov in movimientos:
                if id_vehiculo in self.cancelaciones:
                    await ws_manager.broadcast_to_vehicle(id_vehiculo, {
                        "tipo": "DEMO_CANCELADA",
                        "id_vehiculo": id_vehiculo,
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    })
                    break

                # Actualizar estado (SIN REGISTRAR EN HISTORIAL)
                self.estado_repo.actualizar_estado(id_vehiculo, mov["id_comando"], conectado=True)

                # Emitir movimiento por WebSocket
                await ws_manager.broadcast_to_vehicle(id_vehiculo, {
                    "tipo": "DEMO_MOVIMIENTO",
                    "id_vehiculo": id_vehiculo,
                    "orden": mov["orden"],
                    "comando": mov.get("nombre", mov.get("comando", "N/A")),
                    "codigo": mov["codigo"],
                    "duracion_ms": mov["duracion_ms"],
                    "pausa_ms": mov["pausa_ms"],
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })

                # Temporización sin bloquear el servidor
                if mov["duracion_ms"] > 0:
                    await asyncio.sleep(mov["duracion_ms"] / 1000.0)
                if mov["pausa_ms"] > 0:
                    await asyncio.sleep(mov["pausa_ms"] / 1000.0)

            # 3. Evento de finalización
            if id_vehiculo not in self.cancelaciones:
                await ws_manager.broadcast_to_vehicle(id_vehiculo, {
                    "tipo": "DEMO_FIN",
                    "id_vehiculo": id_vehiculo,
                    "id_demo": id_demo,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
        finally:
            self.demos_activas.discard(id_vehiculo)
            self.cancelaciones.discard(id_vehiculo)

    def cancelar_demo(self, id_vehiculo: int):
        if id_vehiculo in self.demos_activas:
            self.cancelaciones.add(id_vehiculo)
            return {"status": "ok", "mensaje": "Solicitud de cancelación procesada"}
        raise HTTPException(status_code=400, detail="No hay ninguna DEMO activa para este vehículo")

vehicle_service = VehicleService()
