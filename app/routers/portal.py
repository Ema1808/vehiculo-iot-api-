from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime, timezone
from app.models.schemas import UnidadFisicaResponse, ReservaInvitadoRequest, ReservaInvitadoResponse, ModeloVehiculoResponse
from app.repositories.admin_repository import admin_repo
from app.core.security import get_current_user, require_role
from app.core.websocket import ws_manager

router = APIRouter(prefix="/portal", tags=["Portal de Usuarios e Invitados"])

# 1. MIS VEHÍCULOS (USUARIO COMPRADOR)
@router.get("/mis-vehiculos", response_model=List[UnidadFisicaResponse], summary="Consultar vehículos adquiridos por el comprador")
def get_mis_vehiculos(user: dict = Depends(require_role(["USUARIO"]))):
    """Retorna exclusivamente las unidades asignadas a este comprador (Anti-BOLA)."""
    return admin_repo.obtener_unidades_ampliadas(user)

@router.post("/mis-vehiculos/{id_vehiculo}/autorizar-soporte", summary="Otorgar o revocar autorización de soporte a Administrador")
def toggle_soporte(id_vehiculo: int, autoriza: bool, user: dict = Depends(require_role(["USUARIO"]))):
    admin_repo.toggle_autorizacion_soporte(id_vehiculo, user["id_usuario"], autoriza)
    estado_str = "AUTORIZADO" if autoriza else "REVOCADO"
    return {"status": "ok", "mensaje": f"Permiso de control para soporte técnico: {estado_str}"}

# 2. CATÁLOGO PÚBLICO
@router.get("/catalogo-publico", summary="Catálogo comercial accesible para invitados y compradores")
def get_catalogo():
    modelos = admin_repo.obtener_modelos()
    unidades_expo = admin_repo.obtener_unidades_ampliadas({"rol": "INVITADO"})
    return {
        "modelos": modelos,
        "unidades_exhibicion": unidades_expo
    }

# 3. SESIONES TEMPORALES DE INVITADO
@router.post("/invitados/reservar", response_model=ReservaInvitadoResponse, summary="Reservar sesión temporal de prueba en unidad de exhibición")
async def reservar_prueba(req: ReservaInvitadoRequest, user: dict = Depends(require_role(["INVITADO"]))):
    # Validar que el vehículo sea de EXHIBICIÓN
    unidades = admin_repo.obtener_unidades_ampliadas({"rol": "INVITADO"})
    unidad_valida = next((u for u in unidades if u["id_vehiculo"] == req.id_vehiculo), None)
    if not unidad_valida:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La unidad seleccionada no está disponible para pruebas de exhibición"
        )

    # Verificar si ya hay otra sesión activa en este vehículo
    sesion_existente = admin_repo.obtener_sesion_activa_vehiculo(req.id_vehiculo)
    if sesion_existente and sesion_existente["id_usuario_invitado"] != user["id_usuario"]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La unidad de exhibición se encuentra actualmente ocupada por otro visitante. Intente en unos minutos."
        )

    # Reservar por 3 minutos
    reserva = admin_repo.crear_reserva_invitado(user["id_usuario"], req.id_vehiculo, minutos=3)

    # Notificar por WebSocket que la sesión de prueba inició
    await ws_manager.broadcast_to_vehicle(req.id_vehiculo, {
        "tipo": "SESION_INVITADO_INICIO",
        "id_vehiculo": req.id_vehiculo,
        "id_usuario": user["id_usuario"],
        "duracion_segundos": 180,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

    return ReservaInvitadoResponse(**reserva)
