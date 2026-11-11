from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# --- VEHÍCULOS ---
class VehiculoCreate(BaseModel):
    nombre: str = Field(..., max_length=80)
    modelo: Optional[str] = Field(None, max_length=80)
    descripcion: Optional[str] = Field(None, max_length=255)
    microcontrolador: Optional[str] = Field(None, max_length=50)

class VehiculoUpdate(VehiculoCreate):
    activo: bool = True

# --- COMANDOS ---
class ComandoCreate(BaseModel):
    nombre: str = Field(..., max_length=60)
    codigo: int
    descripcion: Optional[str] = Field(None, max_length=255)

class ComandoUpdate(ComandoCreate):
    activo: bool = True

# --- ESTADO Y MOVIMIENTO INDIVIDUAL ---
class MovimientoIndividualRequest(BaseModel):
    id_comando: int
    origen: str = Field("THUNDER-CLIENT", max_length=30)

class EstadoUpdate(BaseModel):
    id_comando: int
    conectado: bool = True

# --- HISTORIAL ---
class HistorialRegistro(BaseModel):
    id_historial: int
    id_vehiculo: int
    id_comando: Optional[int]
    fecha_hora: datetime
    origen: str

# --- DEMOS ---
class DemoCreate(BaseModel):
    nombre: str = Field(..., max_length=80)
    descripcion: Optional[str] = Field(None, max_length=255)

class DemoUpdate(DemoCreate):
    activo: bool = True

class DemoMovimientoCreate(BaseModel):
    id_comando: int
    orden: int
    duracion_ms: int = Field(..., ge=0)
    pausa_ms: int = Field(..., ge=0)

class DemoMovimientoUpdate(DemoMovimientoCreate):
    pass
