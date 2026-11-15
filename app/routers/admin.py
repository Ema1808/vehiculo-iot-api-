from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List
from app.models.schemas import (
    DashboardMetricsResponse, ModeloVehiculoResponse, ModeloVehiculoCreate,
    UnidadFisicaResponse, VehiculoCreate, AsignacionResponse, AsignacionCreate,
    BitacoraResponse, ReservaInvitadoRequest, ReservaInvitadoResponse, UserResponse
)
from app.repositories.admin_repository import admin_repo
from app.core.security import require_role, get_current_user

router = APIRouter(prefix="/admin", tags=["Administración e Inventario"])

# 1. MÉTRICAS DE DASHBOARD (ADMIN)
@router.get("/dashboard/metricas", response_model=DashboardMetricsResponse, summary="Obtener métricas consolidadas del sistema")
def get_dashboard_metrics(admin: dict = Depends(require_role(["ADMINISTRADOR"]))):
    return admin_repo.obtener_metricas_dashboard()

# 2. MODELOS COMERCIALES
@router.get("/modelos", response_model=List[ModeloVehiculoResponse], summary="Listar modelos comerciales de vehículos")
def get_modelos(user: dict = Depends(get_current_user)):
    return admin_repo.obtener_modelos()

@router.post("/modelos", response_model=dict, status_code=status.HTTP_201_CREATED, summary="Crear nuevo modelo comercial")
def create_modelo(req: ModeloVehiculoCreate, request: Request, admin: dict = Depends(require_role(["ADMINISTRADOR"]))):
    mid = admin_repo.crear_modelo(req.nombre, req.categoria, req.descripcion, req.microcontrolador_base)
    client_ip = request.client.host if request.client else "127.0.0.1"
    admin_repo.registrar_auditoria(
        id_usuario=admin["id_usuario"],
        accion="CREAR_MODELO",
        entidad="modelos_vehiculo",
        id_entidad=mid,
        detalle={"nombre": req.nombre, "categoria": req.categoria},
        ip_origen=client_ip
    )
    return {"id_modelo": mid, "mensaje": "Modelo comercial creado exitosamente"}

# 3. UNIDADES FÍSICAS (INVENTARIO)
@router.get("/unidades", response_model=List[UnidadFisicaResponse], summary="Listar inventario de unidades físicas")
def get_unidades_inventario(admin: dict = Depends(require_role(["ADMINISTRADOR"]))):
    return admin_repo.obtener_unidades_ampliadas(admin)

@router.post("/unidades", response_model=dict, status_code=status.HTTP_201_CREATED, summary="Registrar nueva unidad física")
def create_unidad_fisica(req: VehiculoCreate, request: Request, admin: dict = Depends(require_role(["ADMINISTRADOR"]))):
    if not req.numero_serie:
        raise HTTPException(status_code=400, detail="El número de serie es obligatorio para registrar una unidad física")
    
    vid = admin_repo.crear_unidad_fisica(
        id_modelo=req.id_modelo or 1,
        numero_serie=req.numero_serie,
        estado_comercial=req.estado_comercial,
        nombre=req.nombre,
        descripcion=req.descripcion,
        microcontrolador=req.microcontrolador or "ESP32"
    )
    client_ip = request.client.host if request.client else "127.0.0.1"
    admin_repo.registrar_auditoria(
        id_usuario=admin["id_usuario"],
        accion="REGISTRAR_UNIDAD",
        entidad="vehiculos",
        id_entidad=vid,
        detalle={"numero_serie": req.numero_serie, "nombre": req.nombre, "estado": req.estado_comercial},
        ip_origen=client_ip
    )
    return {"id_vehiculo": vid, "mensaje": "Unidad física dada de alta en inventario"}

# 4. CLIENTES Y ASIGNACIONES
@router.get("/clientes", response_model=List[UserResponse], summary="Listar clientes registrados (Compradores)")
def get_clientes(admin: dict = Depends(require_role(["ADMINISTRADOR"]))):
    clientes = admin_repo.obtener_usuarios(id_role=2) # Rol USUARIO
    return [
        UserResponse(
            id_usuario=c["id_usuario"],
            id_role=c["id_role"],
            rol=c["rol"],
            nombre_completo=c["nombre_completo"],
            email=c["email"],
            activo=bool(c["activo"])
        ) for c in clientes
    ]

@router.get("/asignaciones", response_model=List[AsignacionResponse], summary="Consultar asignaciones de vehículos a clientes")
def get_asignaciones(admin: dict = Depends(require_role(["ADMINISTRADOR"]))):
    return admin_repo.obtener_asignaciones()

@router.post("/asignaciones", response_model=dict, status_code=status.HTTP_201_CREATED, summary="Asignar vehículo a un cliente")
def assign_vehiculo(req: AsignacionCreate, request: Request, admin: dict = Depends(require_role(["ADMINISTRADOR"]))):
    asig_id = admin_repo.asignar_vehiculo(req.id_usuario, req.id_vehiculo, req.autoriza_soporte)
    client_ip = request.client.host if request.client else "127.0.0.1"
    admin_repo.registrar_auditoria(
        id_usuario=admin["id_usuario"],
        accion="ASIGNAR_VEHICULO",
        entidad="asignaciones_vehiculo",
        id_entidad=asig_id,
        detalle={"id_usuario": req.id_usuario, "id_vehiculo": req.id_vehiculo},
        ip_origen=client_ip
    )
    return {"id_asignacion": asig_id, "mensaje": "Vehículo asignado exitosamente al cliente"}

# 5. BITÁCORA DE AUDITORÍA
@router.get("/bitacora", response_model=List[BitacoraResponse], summary="Consultar bitácora de auditoría inmutable")
def get_bitacora(limite: int = 50, admin: dict = Depends(require_role(["ADMINISTRADOR"]))):
    return admin_repo.obtener_bitacora(limite)
