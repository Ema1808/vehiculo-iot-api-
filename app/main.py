from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import vehiculos, comandos, estado_historial, demos, ws, auth, admin, portal

app = FastAPI(
    title="API Vehículo Robótico IoT - Ecosistema Empresarial",
    description="API RESTful y WebSocket con POO, RBAC, Control, Monitoreo y Administración integrada con Amazon RDS MySQL",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers de la Plataforma
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(portal.router)
app.include_router(vehiculos.router)
app.include_router(comandos.router)
app.include_router(estado_historial.router)
app.include_router(demos.router)
app.include_router(ws.router)

@app.get("/", tags=["General"])
def root():
    return {
        "sistema": "API Vehículo IoT - Ecosistema Empresarial V2",
        "estado": "En línea",
        "docs": "https://vehiculo-iot-excavadora.duckdns.org/docs",
        "modulos": ["Control", "Monitoreo", "Administración", "RBAC", "WebSocket"]
    }
