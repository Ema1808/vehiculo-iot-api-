from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Any
from datetime import datetime

# --- AUTENTICACIÓN Y USUARIOS ---
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id_usuario: int
    id_role: int
    rol: str
    nombre_completo: str
    email: str
    activo: bool

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class UserCreate(BaseModel):
    id_role: int
    nombre_completo: str = Field(..., max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)

# --- MODELOS COMERCIALES DE VEHÍCULOS ---
class ModeloVehiculoCreate(BaseModel):
    nombre: str = Field(..., max_length=80)
    categoria: str = Field(..., max_length=50)
    descripcion: Optional[str] = Field(None, max_length=255)
    microcontrolador_base: str = Field("ESP32", max_length=50)

class ModeloVehiculoResponse(ModeloVehiculoCreate):
    id_modelo: int
    activo: bool

# --- VEHÍCULOS / UNIDADES FÍSICAS ---
class VehiculoCreate(BaseModel):
    nombre: str = Field(..., max_length=80)
    modelo: Optional[str] = Field(None, max_length=80)
    descripcion: Optional[str] = Field(None, max_length=255)
    microcontrolador: Optional[str] = Field(None, max_length=50)
    id_modelo: Optional[int] = None
    numero_serie: Optional[str] = Field(None, max_length=50)
    estado_comercial: str = Field("DISPONIBLE", max_length=20)

class VehiculoUpdate(VehiculoCreate):
    activo: bool = True

class UnidadFisicaResponse(BaseModel):
    id_vehiculo: int
    id_modelo: Optional[int]
    numero_serie: Optional[str]
    estado_comercial: str
    nombre: str
    modelo: Optional[str]
    descripcion: Optional[str]
    microcontrolador: Optional[str]
    fecha_registro: Optional[datetime]
    activo: bool
    modelo_nombre: Optional[str] = None
    propietario_nombre: Optional[str] = None

# --- ASIGNACIONES DE VEHÍCULOS ---
class AsignacionCreate(BaseModel):
    id_usuario: int
    id_vehiculo: int
    autoriza_soporte: bool = False

class AsignacionUpdate(BaseModel):
    estado: Optional[str] = Field(None, max_length=20)
    autoriza_soporte: Optional[bool] = None

class AsignacionResponse(BaseModel):
    id_asignacion: int
    id_usuario: int
    id_vehiculo: int
    cliente_nombre: str
    cliente_email: str
    vehiculo_nombre: str
    numero_serie: Optional[str]
    fecha_asignacion: datetime
    estado: str
    autoriza_soporte: bool

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

# --- SESIONES DE INVITADO ---
class ReservaInvitadoRequest(BaseModel):
    id_vehiculo: int

class ReservaInvitadoResponse(BaseModel):
    id_sesion: int
    id_vehiculo: int
    token_sesion: str
    inicio: datetime
    fin_programado: datetime
    segundos_restantes: int
    mensaje: str

# --- BITÁCORA Y DASHBOARD ADMIN ---
class BitacoraResponse(BaseModel):
    id_bitacora: int
    id_usuario: Optional[int]
    usuario_nombre: Optional[str]
    accion: str
    entidad_afectada: str
    id_entidad: Optional[int]
    detalle_json: Optional[str]
    ip_origen: Optional[str]
    fecha_hora: datetime

class DashboardMetricsResponse(BaseModel):
    total_modelos: int
    total_unidades: int
    unidades_vendidas: int
    unidades_exhibicion: int
    unidades_disponibles: int
    total_clientes: int
    total_movimientos_historial: int
    demos_totales: int
