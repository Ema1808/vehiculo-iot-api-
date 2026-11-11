from fastapi import APIRouter, status
from app.models.schemas import DemoCreate, DemoUpdate, DemoMovimientoCreate, DemoMovimientoUpdate
from app.repositories.demo_repository import DemoRepository
from app.services.vehicle_service import vehicle_service

router = APIRouter(prefix="/vehiculos/{id_vehiculo}/demos", tags=["Demos y Rutinas"])
demo_repo = DemoRepository()

@router.post("", status_code=status.HTTP_201_CREATED, summary="Crear cabecera de DEMO (sp_crear_demo)")
def crear_demo(id_vehiculo: int, d: DemoCreate):
    """Integra `sp_crear_demo`."""
    id_d = demo_repo.crear_demo(id_vehiculo, d.nombre, d.descripcion)
    return {"id_demo": id_d, "mensaje": "Demo creada exitosamente"}

@router.get("", summary="Listar demos de un vehículo (sp_obtener_demos)")
def obtener_demos(id_vehiculo: int):
    """Integra `sp_obtener_demos`."""
    return demo_repo.obtener_demos(id_vehiculo)

@router.put("/{id_demo}", summary="Actualizar DEMO (sp_actualizar_demo)")
def actualizar_demo(id_demo: int, d: DemoUpdate):
    """Integra `sp_actualizar_demo`."""
    demo_repo.actualizar_demo(id_demo, d.nombre, d.descripcion, d.activo)
    return {"mensaje": "Demo actualizada"}

@router.delete("/{id_demo}", summary="Eliminar DEMO (sp_eliminar_demo)")
def eliminar_demo(id_demo: int):
    """Integra `sp_eliminar_demo`."""
    demo_repo.eliminar_demo(id_demo)
    return {"mensaje": "Demo eliminada"}

@router.post("/{id_demo}/movimientos", status_code=status.HTTP_201_CREATED, summary="Agregar movimiento a DEMO (sp_agregar_movimiento_demo)")
def agregar_movimiento(id_demo: int, m: DemoMovimientoCreate):
    """Integra `sp_agregar_movimiento_demo`."""
    demo_repo.agregar_movimiento(id_demo, m.id_comando, m.orden, m.duracion_ms, m.pausa_ms)
    return {"mensaje": "Movimiento agregado a la DEMO"}

@router.get("/{id_demo}/movimientos", summary="Consultar movimientos de DEMO (sp_obtener_movimientos_demo)")
def obtener_movimientos(id_demo: int):
    """Integra `sp_obtener_movimientos_demo` para consultar los pasos ordenados."""
    return demo_repo.obtener_movimientos(id_demo)

@router.put("/movimientos/{id_demo_movimiento}", summary="Actualizar paso de DEMO (sp_actualizar_movimiento_demo)")
def actualizar_movimiento(id_demo_movimiento: int, m: DemoMovimientoUpdate):
    """Integra `sp_actualizar_movimiento_demo`."""
    demo_repo.actualizar_movimiento(id_demo_movimiento, m.id_comando, m.orden, m.duracion_ms, m.pausa_ms)
    return {"mensaje": "Movimiento de DEMO actualizado"}

@router.delete("/movimientos/{id_demo_movimiento}", summary="Eliminar paso de DEMO (sp_eliminar_movimiento_demo)")
def eliminar_movimiento(id_demo_movimiento: int):
    """Integra `sp_eliminar_movimiento_demo`."""
    demo_repo.eliminar_movimiento(id_demo_movimiento)
    return {"mensaje": "Movimiento de DEMO eliminado"}

@router.post("/{id_demo}/iniciar", summary="Iniciar transmisión de DEMO por WebSocket (Prueba 3)")
async def iniciar_demo(id_vehiculo: int, id_demo: int):
    """
    **Prueba 3 de Thunder Client:**
    Transmite los N movimientos por WebSocket en orden, respetando duración y pausa.
    **NO registra en historial.**
    """
    return await vehicle_service.iniciar_demo_async(id_vehiculo, id_demo)

@router.post("/cancelar", summary="Cancelar DEMO en curso")
def cancelar_demo(id_vehiculo: int):
    """Cancela inmediatamente la emisión de movimientos de una DEMO activa."""
    return vehicle_service.cancelar_demo(id_vehiculo)
