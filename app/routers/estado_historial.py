from fastapi import APIRouter, Depends
from typing import Optional
from app.models.schemas import MovimientoIndividualRequest, EstadoUpdate
from app.services.vehicle_service import vehicle_service
from app.repositories.estado_repository import EstadoRepository
from app.repositories.historial_repository import HistorialRepository
from app.core.security import get_optional_user, verify_vehicle_access

router = APIRouter(prefix="/vehiculos/{id_vehiculo}", tags=["Estado e Historial"])
estado_repo = EstadoRepository()
historial_repo = HistorialRepository()

@router.post("/movimiento", summary="Ejecutar movimiento individual (sp_actualizar_estado + sp_registrar_historial)")
async def registrar_movimiento(id_vehiculo: int, req: MovimientoIndividualRequest, user: Optional[dict] = Depends(get_optional_user)):
    """
    **Prueba 1 de Thunder Client + Control de Acceso RBAC:**
    Ejecuta un movimiento individual atómico:
    1. Si se proporciona token JWT, valida propiedad/soporte (Anti-BOLA).
    2. Valida vehículo y comando.
    3. Llama en una transacción a `sp_actualizar_estado` y `sp_registrar_historial`.
    4. Emite evento por WebSocket.
    """
    if user:
        verify_vehicle_access(id_vehiculo, user, write_access=True)

    return await vehicle_service.ejecutar_movimiento_individual(id_vehiculo, req.id_comando, req.origen)

@router.get("/estado", summary="Consultar último estado (sp_obtener_estado)")
def obtener_estado(id_vehiculo: int):
    """Integra `sp_obtener_estado`."""
    return estado_repo.obtener_estado(id_vehiculo)

@router.put("/estado", summary="Actualizar estado manualmente (sp_actualizar_estado)")
def actualizar_estado(id_vehiculo: int, est: EstadoUpdate):
    """Integra `sp_actualizar_estado` directamente."""
    estado_repo.actualizar_estado(id_vehiculo, est.id_comando, est.conectado)
    return {"mensaje": "Estado actualizado"}

@router.get("/historial", summary="Consultar historial con límite de 10 más recientes (sp_obtener_historial)")
def obtener_historial(id_vehiculo: int):
    """
    **Prueba 2 de Thunder Client:**
    Integra `sp_obtener_historial` y aplica la regla de negocio:
    Devuelve **COMO MÁXIMO diez movimientos individuales más recientes**.
    """
    return historial_repo.obtener_historial(id_vehiculo, limite=10)
