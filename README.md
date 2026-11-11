# API Vehículo Robótico IoT (Práctica 2.5)

API RESTful y WebSocket desarrollada con Python, FastAPI, Programación Orientada a Objetos (POO) y conectada a Amazon RDS (`vehiculo_iot`), integrando 21 Stored Procedures para control de vehículos IoT.

## Arquitectura del Proyecto
```text
vehiculo-iot-api/
├── .env                  # Variables de entorno locales (NO subir a GitHub)
├── .env.example          # Plantilla de configuración pública
├── requirements.txt      # Dependencias del proyecto
└── app/
    ├── core/             # POO: Configuración, Conexión a RDS y WebSocket Manager
    ├── models/           # Esquemas Pydantic para validación de datos
    ├── repositories/     # POO: Clases DAO que encapsulan los 21 Stored Procedures
    ├── services/         # POO: Lógica de negocio, transacciones y ejecución de DEMO
    └── routers/          # Controladores HTTP y WebSocket con Swagger UI
```

## Requisitos Previos
* Python 3.10+
* Instancia Amazon RDS (`vehiculo_iot`) en estado Available con Security Group permitiendo puerto 3306.

## Instrucciones de Ejecución Local

1. **Crear y activar el entorno virtual:**
   ```bash
   python -m venv .venv
   # Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # Linux/Mac:
   source .venv/bin/activate
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno:**
   Copia el archivo `.env.example` como `.env` y coloca las credenciales de tu RDS:
   ```env
   DB_HOST=tu-endpoint-rds.amazonaws.com
   DB_PORT=3306
   DB_USER=admin
   DB_PASSWORD=tu_contraseña
   DB_NAME=vehiculo_iot
   ```

4. **Iniciar el servidor en localhost:8000:**
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

5. **Documentación Swagger UI:**
   Abre tu navegador en: [http://localhost:8000/docs](http://localhost:8000/docs)

## Endpoints de Pruebas Funcionales (Thunder Client)

1. **Prueba 1 (POST Movimiento Individual):**
   * `POST http://localhost:8000/vehiculos/1/movimiento`
   * Body: `{"id_comando": 1, "origen": "THUNDER-CLIENT"}`
2. **Prueba 2 (GET Historial 10 más recientes):**
   * `GET http://localhost:8000/vehiculos/1/historial`
3. **Prueba 3 (WebSocket + Inicio DEMO):**
   * WebSocket: `ws://localhost:8000/ws/vehiculos/1`
   * Disparo HTTP: `POST http://localhost:8000/vehiculos/1/demos/1/iniciar`
