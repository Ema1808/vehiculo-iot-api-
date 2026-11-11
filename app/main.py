from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import vehiculos, comandos, estado_historial, demos, ws

app = FastAPI(
    title="API Vehículo Robótico IoT",
    description="API RESTful y WebSocket con POO integrada con los 21 Stored Procedures en Amazon RDS",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Habilitar CORS para pruebas locales
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar Routers
app.include_router(vehiculos.router)
app.include_router(comandos.router)
app.include_router(estado_historial.router)
app.include_router(demos.router)
app.include_router(ws.router)

@app.get("/", tags=["General"])
def root():
    return {
        "sistema": "API Vehículo IoT - Entorno Dev",
        "estado": "En línea",
        "docs": "http://localhost:8000/docs",
        "ws": "ws://localhost:8000/ws/vehiculos/{id_vehiculo}"
    }
