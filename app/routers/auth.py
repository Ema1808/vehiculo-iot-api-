from fastapi import APIRouter, HTTPException, status, Request, Depends
from app.models.schemas import LoginRequest, TokenResponse, UserResponse
from app.repositories.admin_repository import admin_repo
from app.core.security import verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Autenticación y Sesiones"])

@router.post("/login", response_model=TokenResponse, summary="Iniciar sesión y obtener token JWT")
def login(req: LoginRequest, request: Request):
    """
    Autentica usuario por email y contraseña.
    Devuelve JWT con Claims: sub (id_usuario), rol, email.
    """
    user = admin_repo.obtener_usuario_por_email(req.email)
    if not user or not user.get("activo"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos"
        )
    
    if not verify_password(req.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo electrónico o contraseña incorrectos"
        )
    
    # Crear Token JWT
    token_data = {
        "sub": str(user["id_usuario"]),
        "rol": user["rol"],
        "email": user["email"]
    }
    token = create_access_token(token_data)

    # Registrar en bitácora
    client_ip = request.client.host if request.client else "127.0.0.1"
    admin_repo.registrar_auditoria(
        id_usuario=user["id_usuario"],
        accion="LOGIN_EXITOSO",
        entidad="usuarios",
        id_entidad=user["id_usuario"],
        detalle={"email": user["email"], "rol": user["rol"]},
        ip_origen=client_ip
    )

    user_resp = UserResponse(
        id_usuario=user["id_usuario"],
        id_role=user["id_role"],
        rol=user["rol"],
        nombre_completo=user["nombre_completo"],
        email=user["email"],
        activo=bool(user["activo"])
    )

    return TokenResponse(access_token=token, token_type="bearer", user=user_resp)

@router.get("/me", response_model=UserResponse, summary="Obtener perfil de usuario activo")
def get_me(user: dict = Depends(get_current_user)):
    """Devuelve la información del usuario autenticado."""
    return UserResponse(
        id_usuario=user["id_usuario"],
        id_role=user["id_role"],
        rol=user["rol"],
        nombre_completo=user["nombre_completo"],
        email=user["email"],
        activo=bool(user["activo"])
    )

@router.post("/logout", summary="Cerrar sesión")
def logout(request: Request, user: dict = Depends(get_current_user)):
    """Registra cierre de sesión en bitácora de auditoría."""
    client_ip = request.client.host if request.client else "127.0.0.1"
    admin_repo.registrar_auditoria(
        id_usuario=user["id_usuario"],
        accion="LOGOUT",
        entidad="usuarios",
        id_entidad=user["id_usuario"],
        detalle={"email": user["email"]},
        ip_origen=client_ip
    )
    return {"status": "ok", "mensaje": "Sesión finalizada exitosamente"}
