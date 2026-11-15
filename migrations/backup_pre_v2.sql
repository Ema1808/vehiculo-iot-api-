-- Respaldo previo a migracion V2 generado automaticamente
-- Base de datos: vehiculo_iot

-- Datos de la tabla `comandos` (9 registros)
INSERT IGNORE INTO `comandos` (`id_comando`, `id_vehiculo`, `nombre`, `codigo`, `descripcion`, `activo`) VALUES (1, 1, 'AVANZAR', 1, 'Mover el vehículo hacia adelante', 1);
INSERT IGNORE INTO `comandos` (`id_comando`, `id_vehiculo`, `nombre`, `codigo`, `descripcion`, `activo`) VALUES (2, 1, 'RETROCEDER', 2, 'Mover el vehículo hacia atrás', 1);
INSERT IGNORE INTO `comandos` (`id_comando`, `id_vehiculo`, `nombre`, `codigo`, `descripcion`, `activo`) VALUES (3, 1, 'GIRAR_IZQUIERDA', 3, 'Giro hacia la izquierda', 1);
INSERT IGNORE INTO `comandos` (`id_comando`, `id_vehiculo`, `nombre`, `codigo`, `descripcion`, `activo`) VALUES (4, 1, 'GIRAR_DERECHA', 4, 'Giro hacia la derecha', 1);
INSERT IGNORE INTO `comandos` (`id_comando`, `id_vehiculo`, `nombre`, `codigo`, `descripcion`, `activo`) VALUES (5, 1, 'SUBIR_BRAZO', 5, 'Elevar el brazo', 1);
INSERT IGNORE INTO `comandos` (`id_comando`, `id_vehiculo`, `nombre`, `codigo`, `descripcion`, `activo`) VALUES (6, 1, 'BAJAR_BRAZO', 6, 'Descender el brazo', 1);
INSERT IGNORE INTO `comandos` (`id_comando`, `id_vehiculo`, `nombre`, `codigo`, `descripcion`, `activo`) VALUES (7, 1, 'ABRIR_PALA', 7, 'Abrir la pala', 1);
INSERT IGNORE INTO `comandos` (`id_comando`, `id_vehiculo`, `nombre`, `codigo`, `descripcion`, `activo`) VALUES (8, 1, 'CERRAR_PALA', 8, 'Cerrar la pala', 1);
INSERT IGNORE INTO `comandos` (`id_comando`, `id_vehiculo`, `nombre`, `codigo`, `descripcion`, `activo`) VALUES (9, 1, 'DETENER', 9, 'Detener cualquier movimiento', 1);

-- Datos de la tabla `demo_movimientos` (8 registros)
INSERT IGNORE INTO `demo_movimientos` (`id_demo_movimiento`, `id_demo`, `id_comando`, `orden`, `duracion_ms`, `pausa_ms`) VALUES (1, 1, 1, 1, 2000, 400);
INSERT IGNORE INTO `demo_movimientos` (`id_demo_movimiento`, `id_demo`, `id_comando`, `orden`, `duracion_ms`, `pausa_ms`) VALUES (2, 1, 3, 2, 1000, 300);
INSERT IGNORE INTO `demo_movimientos` (`id_demo_movimiento`, `id_demo`, `id_comando`, `orden`, `duracion_ms`, `pausa_ms`) VALUES (3, 1, 5, 3, 1500, 300);
INSERT IGNORE INTO `demo_movimientos` (`id_demo_movimiento`, `id_demo`, `id_comando`, `orden`, `duracion_ms`, `pausa_ms`) VALUES (4, 1, 7, 4, 900, 250);
INSERT IGNORE INTO `demo_movimientos` (`id_demo_movimiento`, `id_demo`, `id_comando`, `orden`, `duracion_ms`, `pausa_ms`) VALUES (5, 1, 8, 5, 900, 250);
INSERT IGNORE INTO `demo_movimientos` (`id_demo_movimiento`, `id_demo`, `id_comando`, `orden`, `duracion_ms`, `pausa_ms`) VALUES (6, 1, 6, 6, 1500, 300);
INSERT IGNORE INTO `demo_movimientos` (`id_demo_movimiento`, `id_demo`, `id_comando`, `orden`, `duracion_ms`, `pausa_ms`) VALUES (7, 1, 2, 7, 2000, 400);
INSERT IGNORE INTO `demo_movimientos` (`id_demo_movimiento`, `id_demo`, `id_comando`, `orden`, `duracion_ms`, `pausa_ms`) VALUES (8, 1, 9, 8, 500, 0);

-- Datos de la tabla `demos` (1 registros)
INSERT IGNORE INTO `demos` (`id_demo`, `id_vehiculo`, `id_usuario_creador`, `nombre`, `descripcion`, `activo`) VALUES (1, 1, NULL, 'Demo principal', 'Secuencia automática de movimientos del vehículo', 1);

-- Datos de la tabla `estado_vehiculo` (1 registros)
INSERT IGNORE INTO `estado_vehiculo` (`id_estado`, `id_vehiculo`, `id_comando`, `fecha_actualizacion`, `conectado`) VALUES (1, 1, 4, '2026-11-11 20:46:10', 1);

-- Datos de la tabla `historial_comandos` (88 registros)
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (1, 1, 1, '2026-11-11 17:07:37', 'VSCODE-RDS');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (2, 1, 3, '2026-11-11 17:07:37', 'VSCODE-RDS');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (3, 1, 5, '2026-11-11 17:07:37', 'VSCODE-RDS');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (4, 1, 7, '2026-11-11 17:07:37', 'VSCODE-RDS');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (5, 1, 9, '2026-11-11 17:07:37', 'VSCODE-RDS');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (6, 1, 1, '2026-11-11 17:35:01', 'THUNDER-CLIENT');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (7, 1, 1, '2026-11-11 17:38:01', 'THUNDER-CLIENT');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (8, 1, 1, '2026-11-11 18:36:32', 'EXAMEN-REMOTO-2.6');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (9, 1, 3, '2026-11-11 19:52:02', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (10, 1, 1, '2026-11-11 19:52:05', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (11, 1, 2, '2026-11-11 19:52:06', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (12, 1, 9, '2026-11-11 19:52:06', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (13, 1, 2, '2026-11-11 19:52:06', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (14, 1, 9, '2026-11-11 19:52:06', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (15, 1, 4, '2026-11-11 19:56:39', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (16, 1, 9, '2026-11-11 19:56:40', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (17, 1, 3, '2026-11-11 19:56:41', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (18, 1, 9, '2026-11-11 19:56:41', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (19, 1, 9, '2026-11-11 19:56:42', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (20, 1, 1, '2026-11-11 19:56:45', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (21, 1, 9, '2026-11-11 19:56:45', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (22, 1, 3, '2026-11-11 19:56:46', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (23, 1, 9, '2026-11-11 19:56:46', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (24, 1, 5, '2026-11-11 19:57:02', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (25, 1, 7, '2026-11-11 19:57:03', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (26, 1, 8, '2026-11-11 19:57:04', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (27, 1, 6, '2026-11-11 19:57:05', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (28, 1, 4, '2026-11-11 19:58:54', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (29, 1, 9, '2026-11-11 19:58:54', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (30, 1, 4, '2026-11-11 19:58:55', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (31, 1, 9, '2026-11-11 19:58:55', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (32, 1, 2, '2026-11-11 19:58:56', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (33, 1, 9, '2026-11-11 19:58:56', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (34, 1, 5, '2026-11-11 19:59:38', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (35, 1, 7, '2026-11-11 19:59:39', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (36, 1, 8, '2026-11-11 19:59:39', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (37, 1, 6, '2026-11-11 19:59:40', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (38, 1, 5, '2026-11-11 19:59:41', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (39, 1, 9, '2026-11-11 19:59:43', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (40, 1, 1, '2026-11-11 19:59:45', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (41, 1, 9, '2026-11-11 19:59:45', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (42, 1, 2, '2026-11-11 19:59:46', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (43, 1, 9, '2026-11-11 19:59:46', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (44, 1, 2, '2026-11-11 19:59:48', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (45, 1, 9, '2026-11-11 19:59:48', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (46, 1, 9, '2026-11-11 19:59:49', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (47, 1, 3, '2026-11-11 19:59:50', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (48, 1, 9, '2026-11-11 19:59:50', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (49, 1, 1, '2026-11-11 19:59:52', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (50, 1, 9, '2026-11-11 19:59:52', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (51, 1, 1, '2026-11-11 19:59:53', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (52, 1, 9, '2026-11-11 19:59:54', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (53, 1, 2, '2026-11-11 19:59:55', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (54, 1, 9, '2026-11-11 19:59:56', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (55, 1, 4, '2026-11-11 20:00:14', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (56, 1, 4, '2026-11-11 20:00:16', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (57, 1, 4, '2026-11-11 20:00:16', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (58, 1, 3, '2026-11-11 20:00:18', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (59, 1, 1, '2026-11-11 20:00:19', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (60, 1, 3, '2026-11-11 20:12:03', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (61, 1, 4, '2026-11-11 20:12:04', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (62, 1, 2, '2026-11-11 20:12:04', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (63, 1, 5, '2026-11-11 20:12:15', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (64, 1, 5, '2026-11-11 20:12:16', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (65, 1, 4, '2026-11-11 20:16:34', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (66, 1, 3, '2026-11-11 20:16:37', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (67, 1, 9, '2026-11-11 20:16:38', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (68, 1, 5, '2026-11-11 20:17:00', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (69, 1, 6, '2026-11-11 20:17:03', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (70, 1, 8, '2026-11-11 20:17:05', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (71, 1, 7, '2026-11-11 20:17:07', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (72, 1, 9, '2026-11-11 20:17:59', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (73, 1, 3, '2026-11-11 20:18:04', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (74, 1, 9, '2026-11-11 20:18:05', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (75, 1, 1, '2026-11-11 20:18:06', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (76, 1, 9, '2026-11-11 20:18:07', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (77, 1, 2, '2026-11-11 20:18:07', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (78, 1, 9, '2026-11-11 20:18:08', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (79, 1, 4, '2026-11-11 20:18:09', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (80, 1, 9, '2026-11-11 20:18:10', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (81, 1, 4, '2026-11-11 20:21:06', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (82, 1, 5, '2026-11-11 20:21:13', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (83, 1, 6, '2026-11-11 20:21:17', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (84, 1, 8, '2026-11-11 20:21:19', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (85, 1, 7, '2026-11-11 20:21:21', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (86, 1, 4, '2026-11-11 20:36:20', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (87, 1, 4, '2026-11-11 20:43:59', 'WEB-CONTROL');
INSERT IGNORE INTO `historial_comandos` (`id_historial`, `id_vehiculo`, `id_comando`, `fecha_hora`, `origen`) VALUES (88, 1, 4, '2026-11-11 20:46:10', 'WEB-CONTROL');

-- Datos de la tabla `vehiculos` (1 registros)
INSERT IGNORE INTO `vehiculos` (`id_vehiculo`, `id_modelo`, `nombre`, `modelo`, `descripcion`, `microcontrolador`, `fecha_registro`, `activo`) VALUES (1, NULL, 'Excavadora IoT', 'Modelo X', 'Vehículo de construcción controlado por ESP8266', 'ESP8266', '2026-11-11 17:06:35', 1);

