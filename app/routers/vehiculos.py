from fastapi import APIRouter, HTTPException, status
from app.models.schemas import VehiculoCreate, VehiculoUpdate
from app.repositories.vehiculo_repository import VehiculoRepository

router = APIRouter(prefix="/vehiculos", tags=["Vehículos"])
repo = VehiculoRepository()

@router.post("", status_code=status.HTTP_201_CREATED, summary="Crear un vehículo (sp_crear_vehiculo)")
def crear_vehiculo(v: VehiculoCreate):
    """Integra `sp_crear_vehiculo` para dar de alta un chasis o robot."""
    id_v = repo.crear(v.nombre, v.modelo, v.descripcion, v.microcontrolador)
    return {"id_vehiculo": id_v, "mensaje": "Vehículo creado exitosamente"}

@router.get("", summary="Obtener todos los vehículos (sp_obtener_vehiculos)")
def obtener_vehiculos():
    """Integra `sp_obtener_vehiculos` para listar el parque de vehículos IoT."""
    return repo.obtener_todos()

@router.get("/{id_vehiculo}", summary="Obtener vehículo por ID (sp_obtener_vehiculo)")
def obtener_vehiculo(id_vehiculo: int):
    """Integra `sp_obtener_vehiculo` para consultar un vehículo específico."""
    res = repo.obtener_por_id(id_vehiculo)
    if not res:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return res

@router.put("/{id_vehiculo}", summary="Actualizar vehículo (sp_actualizar_vehiculo)")
def actualizar_vehiculo(id_vehiculo: int, v: VehiculoUpdate):
    """Integra `sp_actualizar_vehiculo`."""
    repo.actualizar(id_vehiculo, v.nombre, v.modelo, v.descripcion, v.microcontrolador, v.activo)
    return {"mensaje": "Vehículo actualizado"}

@router.delete("/{id_vehiculo}", summary="Eliminar vehículo (sp_eliminar_vehiculo)")
def eliminar_vehiculo(id_vehiculo: int):
    """Integra `sp_eliminar_vehiculo`."""
    repo.eliminar(id_vehiculo)
    return {"mensaje": "Vehículo eliminado"}
