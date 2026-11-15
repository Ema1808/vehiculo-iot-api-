import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, List
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.core.database import db_manager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

def hash_password(password: str) -> str:
    """Genera hash SHA-256 con salt configurable."""
    salted = settings.PASSWORD_SALT + password
    return hashlib.sha256(salted.encode("utf-8")).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña coincide con el hash almacenado."""
    return hash_password(plain_password) == hashed_password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Emite un token JWT con tiempo de expiración y claims."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """Decodifica y valida un token JWT."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token de sesión ha expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación inválido",
            headers={"WWW-Authenticate": "Bearer"}
        )

async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)) -> dict:
    """Dependencia de inyección de usuario autenticado."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación no proporcionadas",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token no contiene identificador de usuario")

    with db_manager.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT u.id_usuario, u.id_role, r.nombre AS rol, u.nombre_completo, u.email, u.activo
                  FROM usuarios u
                  JOIN roles r ON u.id_role = r.id_role
                 WHERE u.id_usuario = %s AND u.activo = 1
            """, (user_id,))
            user = cur.fetchone()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado o inactivo")
    
    return user

async def get_optional_user(token: Optional[str] = Depends(oauth2_scheme)) -> Optional[dict]:
    """Para compatibilidad con peticiones que no requieren login obligatorio."""
    if not token:
        return None
    try:
        return await get_current_user(token)
    except HTTPException:
        return None

def require_role(allowed_roles: List[str]):
    """Fábrica de dependencias RBAC."""
    def role_checker(user: dict = Depends(get_current_user)) -> dict:
        if user["rol"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permisos insuficientes. Se requiere uno de los siguientes roles: {', '.join(allowed_roles)}"
            )
        return user
    return role_checker

def verify_vehicle_access(id_vehiculo: int, user: dict, write_access: bool = False) -> dict:
    """
    Verifica autorización por recurso (propiedad/asignación) para prevenir IDOR/BOLA.
    Retorna los datos del vehículo si el acceso es concedido.
    """
    with db_manager.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM vehiculos WHERE id_vehiculo = %s", (id_vehiculo,))
            vehiculo = cur.fetchone()
            if not vehiculo:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehículo #{id_vehiculo} no encontrado")

            rol = user["rol"]
            user_id = user["id_usuario"]

            # 1. Reglas para ADMINISTRADOR
            if rol == "ADMINISTRADOR":
                if write_access and vehiculo.get("estado_comercial") == "VENDIDO":
                    # Comprobar si el comprador otorgó autorización explícita de soporte
                    cur.execute("""
                        SELECT autoriza_soporte FROM asignaciones_vehiculo
                         WHERE id_vehiculo = %s AND estado = 'ACTIVA'
                    """, (id_vehiculo,))
                    asig = cur.fetchone()
                    if not asig or not asig.get("autoriza_soporte"):
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="El Administrador no puede operar el control de un vehículo vendido sin autorización explícita de soporte del comprador."
                        )
                return vehiculo

            # 2. Reglas para USUARIO (Comprador)
            if rol == "USUARIO":
                cur.execute("""
                    SELECT id_asignacion FROM asignaciones_vehiculo
                     WHERE id_usuario = %s AND id_vehiculo = %s AND estado = 'ACTIVA'
                """, (user_id, id_vehiculo))
                asig = cur.fetchone()
                if not asig:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Acceso denegado: este vehículo no pertenece a su cuenta de usuario."
                    )
                return vehiculo

            # 3. Reglas para INVITADO
            if rol == "INVITADO":
                if vehiculo.get("estado_comercial") != "EXHIBICION":
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Los invitados solo pueden acceder a unidades designadas para EXHIBICIÓN."
                    )
                if write_access:
                    cur.execute("""
                        SELECT id_sesion FROM sesiones_invitado
                         WHERE id_usuario_invitado = %s AND id_vehiculo = %s
                           AND estado = 'ACTIVA' AND fin_programado > NOW()
                    """, (user_id, id_vehiculo))
                    sesion = cur.fetchone()
                    if not sesion:
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="Acceso denegado: requiere una reserva de sesión de prueba activa para operar este vehículo."
                        )
                return vehiculo

            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Rol de usuario no autorizado")
