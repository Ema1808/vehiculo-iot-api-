from fastapi import APIRouter, status
from app.models.schemas import ComandoCreate, ComandoUpdate
from app.repositories.comando_repository import ComandoRepository

router = APIRouter(prefix="/vehiculos/{id_vehiculo}/comandos", tags=["Comandos"])
repo = ComandoRepository()

@router.post("", status_code=status.HTTP_201_CREATED, summary="Crear comando (sp_crear_comando)")
def crear_comando(id_vehiculo: int, c: ComandoCreate):
    """Integra `sp_crear_comando` para registrar una instrucción que el vehículo comprende."""
    id_cmd = repo.crear(id_vehiculo, c.nombre, c.codigo, c.descripcion)
    return {"id_comando": id_cmd, "mensaje": "Comando creado exitosamente"}

@router.get("", summary="Listar comandos de un vehículo (sp_obtener_comandos_vehiculo)")
def obtener_comandos(id_vehiculo: int):
    """Integra `sp_obtener_comandos_vehiculo`."""
    return repo.obtener_por_vehiculo(id_vehiculo)

@router.put("/{id_comando}", summary="Actualizar comando (sp_actualizar_comando)")
def actualizar_comando(id_comando: int, c: ComandoUpdate):
    """Integra `sp_actualizar_comando`."""
    repo.actualizar(id_comando, c.nombre, c.codigo, c.descripcion, c.activo)
    return {"mensaje": "Comando actualizado"}

@router.delete("/{id_comando}", summary="Eliminar comando (sp_eliminar_comando)")
def eliminar_comando(id_comando: int):
    """Integra `sp_eliminar_comando`."""
    repo.eliminar(id_comando)
    return {"mensaje": "Comando eliminado"}
