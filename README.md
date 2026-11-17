# API Vehículo IoT · Ecosistema Empresarial V2 (FastAPI + RDS + WebSockets)

API RESTful y WebSocket segura desarrollada con **Python 3.12**, **FastAPI**, Programación Orientada a Objetos (POO), arquitectura en capas, control de acceso basado en roles (**RBAC**), autorización por recurso (**Anti-BOLA/IDOR**) y conectada a **Amazon RDS for MySQL** (`vehiculo_iot`).

* **Documentación Interactiva Swagger:** [https://vehiculo-iot-excavadora.duckdns.org/docs](https://vehiculo-iot-excavadora.duckdns.org/docs)
* **Canal WebSocket Seguro:** `wss://vehiculo-iot-excavadora.duckdns.org/ws/vehiculos/{id_vehiculo}`
* **Desarrollado por:** Emanuel González Mayorga · 2026

---

## 1. Arquitectura de Software en Capas

```plaintext
vehiculo-iot-api/
├── .env.example              # Plantilla pública de variables de entorno (sin secretos)
├── .gitignore                # Exclusión de .env, .venv, caches y logs
├── requirements.txt          # Dependencias (FastAPI, Uvicorn, PyMySQL, PyJWT, etc.)
├── migrations/               # Migraciones SQL versionadas para Amazon RDS
│   ├── backup_pre_v2.sql     # Script de respaldo previo a la migración V2
│   ├── V2__migracion_administracion_UP.sql   # Migración no destructiva idempotente
│   ├── V2__migracion_administracion_DOWN.sql # Plan de reversión seguro
│   └── run_migrations.py     # Ejecutor automatizado de migraciones con logging
└── app/
    ├── main.py               # Instancia de FastAPI, CORS y registro de routers
    ├── core/
    │   ├── config.py         # Carga robusta de configuración y JWT
    │   ├── database.py       # Conexión pool y context manager para Amazon RDS MySQL
    │   ├── security.py       # Hashing de contraseñas, encode/decode JWT y verificación Anti-IDOR
    │   └── ws_manager.py     # Gestor de conexiones WebSocket por vehículo y difusión
    ├── models/
    │   └── schemas.py        # Esquemas Pydantic v2 (Auth, Modelos, Unidades, Asignaciones, Demos)
    ├── repositories/
    │   ├── admin_repository.py      # Operaciones de base de datos para Administración y RBAC
    │   ├── comando_repository.py    # Stored Procedures para comandos
    │   ├── demo_repository.py       # Stored Procedures para rutinas DEMO
    │   ├── estado_repository.py     # Stored Procedures para estado e historial
    │   └── vehiculo_repository.py   # Stored Procedures para vehículos
    ├── services/
    │   └── demo_service.py   # Orquestador asíncrono de rutinas DEMO en segundo plano
    └── routers/
        ├── admin.py          # Dashboard de métricas, modelos, unidades, clientes, asignaciones, bitácora
        ├── auth.py           # Login, me y logout con JWT Bearer Tokens
        ├── portal.py         # Mis vehículos, autorizar soporte, catálogo público y reservas
        ├── comandos.py       # CRUD de comandos (reutilizado 4.1)
        ├── demos.py          # Control de DEMO (reutilizado 4.1)
        ├── estado_historial.py # Movimientos individuales, estado e historial (4.1 y 4.2)
        ├── vehiculos.py      # Consulta de vehículos (reutilizado 4.1)
        └── ws.py             # Canal WebSocket seguro con validación opcional de token
```

---

## 2. Modelo de Base de Datos (12 Tablas en Amazon RDS)

El esquema conserva las 6 tablas históricas de las prácticas 4.1 y 4.2 y añade 6 tablas no destructivas para la Práctica 4.3:

1. **`roles`:** Catálogo de roles del sistema (`ADMINISTRADOR`, `USUARIO`, `INVITADO`).
2. **`usuarios`:** Clientes y administradores con credenciales hasheadas (`SHA-256 + salt`).
3. **`modelos_vehiculo`:** Catálogo comercial de modelos y especificaciones de microcontrolador.
4. **`vehiculos`:** Unidades físicas con número de serie, modelo comercial asociado y estado (`DISPONIBLE`, `VENDIDO`, `EXHIBICION`).
5. **`asignaciones_vehiculo`:** Relación cliente-unidad con bandera de autorización de soporte (`autoriza_soporte`).
6. **`sesiones_invitado`:** Reservas temporales exclusivas de 180 segundos en unidades de exhibición.
7. **`bitacora_auditoria`:** Registro de acciones administrativas sensibles con actor, fecha/hora e IP.
8. **`comandos`:** Catálogo de comandos de hardware (incluyendo `LUCES` #10 y `SONIDO` #11).
9. **`estado_vehiculo`:** Último comando y estado de conexión persistido en RDS.
10. **`historial_comandos`:** Registro transaccional de movimientos individuales.
11. **`demos`:** Rutinas de demostración autónomas (con campos `id_usuario_creador` y `es_fabrica`).
12. **`demo_movimientos`:** Secuencia ordenada de pasos y tiempos por rutina.

---

## 3. Seguridad y Autorización por Recurso (Anti-BOLA/IDOR)

El backend no delega la seguridad en la interfaz:
* **Autenticación:** Tokens JWT con firma `HS256` y expiración configurada.
* **Control de Acceso Basado en Roles (RBAC):** Dependencia `require_role(["ADMINISTRADOR"])` en endpoints administrativos.
* **Aislamiento por Recurso (`verify_vehicle_access`):**
  * Un **Usuario** sólo puede consultar y operar unidades que le pertenezcan según la tabla `asignaciones_vehiculo`. Intentar enviar comandos o consultar telemetría de una unidad ajena responde inmediatamente con `403 Forbidden`.
  * El **Administrador** no puede operar una unidad vendida a menos que el comprador haya activado explícitamente `autoriza_soporte = 1`.
  * El **Invitado** sólo puede operar la unidad de exhibición `#2` si cuenta con una reserva activa en `sesiones_invitado`.
