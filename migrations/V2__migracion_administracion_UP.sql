-- =============================================================================
-- MIGRACIÓN V2: MÓDULO DE ADMINISTRACIÓN IoT + RBAC + ASIGNACIONES + AUDITORÍA
-- Base de datos: vehiculo_iot (Amazon RDS MySQL)
-- Script: UP (Aplicación de cambios no destructivos)
-- =============================================================================

USE `vehiculo_iot`;

-- -----------------------------------------------------------------------------
-- 1. TABLA: roles
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `roles` (
  `id_role` INT NOT NULL,
  `nombre` VARCHAR(30) NOT NULL UNIQUE,
  `descripcion` VARCHAR(255) NULL,
  PRIMARY KEY (`id_role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `roles` (`id_role`, `nombre`, `descripcion`) VALUES
(1, 'ADMINISTRADOR', 'Empresa vendedora: gestión de modelos, inventario, clientes y auditoría'),
(2, 'USUARIO', 'Comprador: acceso exclusivo a sus unidades adquiridas y demos privadas'),
(3, 'INVITADO', 'Cliente potencial: consulta de catálogo público y prueba temporal de exhibición');

-- -----------------------------------------------------------------------------
-- 2. TABLA: usuarios
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id_usuario` INT NOT NULL AUTO_INCREMENT,
  `id_role` INT NOT NULL,
  `nombre_completo` VARCHAR(100) NOT NULL,
  `email` VARCHAR(100) NOT NULL UNIQUE,
  `password_hash` VARCHAR(255) NOT NULL,
  `activo` TINYINT(1) NOT NULL DEFAULT 1,
  `fecha_registro` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_usuario`),
  KEY `fk_usuario_role` (`id_role`),
  CONSTRAINT `fk_usuario_role` FOREIGN KEY (`id_role`) REFERENCES `roles` (`id_role`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Usuarios semilla con contraseñas:
-- admin@iot.com      -> admin123
-- comprador@iot.com  -> comprador123
-- invitado@iot.com   -> invitado123
INSERT IGNORE INTO `usuarios` (`id_usuario`, `id_role`, `nombre_completo`, `email`, `password_hash`, `activo`) VALUES
(1, 1, 'Administrador de Planta IoT', 'admin@iot.com', '302c386bd0be0219289ff243d88afceb2acddb81e64cfe70084ed6131051f440', 1),
(2, 2, 'Emmanuel González Mayorga', 'comprador@iot.com', 'adbab55385c83f9033daf1dd4514a859e6aa3c714e596f377e0522cbe8fda3eb', 1),
(3, 3, 'Cliente Potencial Invitado', 'invitado@iot.com', '69bcd6efe656ac24a9eca5f426e902374167773c1fe48c5d4e93f63557565179', 1);

-- -----------------------------------------------------------------------------
-- 3. TABLA: modelos_vehiculo
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `modelos_vehiculo` (
  `id_modelo` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(80) NOT NULL,
  `categoria` VARCHAR(50) NOT NULL,
  `descripcion` VARCHAR(255) NULL,
  `microcontrolador_base` VARCHAR(50) DEFAULT 'ESP32',
  `activo` TINYINT(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id_modelo`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT IGNORE INTO `modelos_vehiculo` (`id_modelo`, `nombre`, `categoria`, `descripcion`, `microcontrolador_base`, `activo`) VALUES
(1, 'Excavadora Minera IoT', 'Maquinaria Pesada', 'Excavadora industrial a escala con brazo mecánico, pala y tracción oruga', 'ESP32 38-pin', 1),
(2, 'Rover Explorador 4WD', 'Exploración Terrestre', 'Vehículo de exploración autónomo con tracción diferencial y sensores', 'ESP32 DevKit', 1),
(3, 'Grúa Industrial IoT', 'Izaje y Carga', 'Grúa de torre motorizada con tornamesa 360 grados y sistema de izaje', 'ESP32 DevKit', 1);

-- -----------------------------------------------------------------------------
-- 4. AMPLIACIÓN NO DESTRUCTIVA: vehiculos
-- -----------------------------------------------------------------------------
-- Procedimiento temporal para añadir columnas sólo si no existen
DROP PROCEDURE IF EXISTS `_sp_migrar_vehiculos_v2`;
DELIMITER ;;
CREATE PROCEDURE `_sp_migrar_vehiculos_v2`()
BEGIN
    IF NOT EXISTS (
        SELECT * FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'vehiculos' AND COLUMN_NAME = 'id_modelo'
    ) THEN
        ALTER TABLE `vehiculos` ADD COLUMN `id_modelo` INT NULL AFTER `id_vehiculo`;
        ALTER TABLE `vehiculos` ADD CONSTRAINT `fk_vehiculo_modelo` FOREIGN KEY (`id_modelo`) REFERENCES `modelos_vehiculo` (`id_modelo`) ON DELETE SET NULL ON UPDATE CASCADE;
    END IF;

    IF NOT EXISTS (
        SELECT * FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'vehiculos' AND COLUMN_NAME = 'numero_serie'
    ) THEN
        ALTER TABLE `vehiculos` ADD COLUMN `numero_serie` VARCHAR(50) NULL AFTER `id_modelo`;
        ALTER TABLE `vehiculos` ADD UNIQUE KEY `uq_vehiculo_serie` (`numero_serie`);
    END IF;

    IF NOT EXISTS (
        SELECT * FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'vehiculos' AND COLUMN_NAME = 'estado_comercial'
    ) THEN
        ALTER TABLE `vehiculos` ADD COLUMN `estado_comercial` VARCHAR(20) NOT NULL DEFAULT 'DISPONIBLE' AFTER `numero_serie`;
    END IF;
END ;;
DELIMITER ;

CALL `_sp_migrar_vehiculos_v2`();
DROP PROCEDURE IF EXISTS `_sp_migrar_vehiculos_v2`;

-- Sincronizar el vehículo existente (ID 1 = Excavadora IoT)
UPDATE `vehiculos`
   SET `id_modelo` = 1,
       `numero_serie` = 'EXC-2026-001',
       `estado_comercial` = 'VENDIDO'
 WHERE `id_vehiculo` = 1 AND (`numero_serie` IS NULL OR `numero_serie` = '');

-- Unidad de exhibición para pruebas de invitados (ID 2 = Unidad Demo)
INSERT IGNORE INTO `vehiculos` (`id_vehiculo`, `id_modelo`, `numero_serie`, `estado_comercial`, `nombre`, `modelo`, `descripcion`, `microcontrolador`, `activo`)
VALUES (2, 1, 'EXC-DEMO-EXPO', 'EXHIBICION', 'Excavadora Expo (Unidad de Prueba)', 'Excavadora Minera', 'Unidad de exhibición reservable para demostración temporal', 'ESP32 38-pin', 1);

-- Duplicar comandos básicos en la unidad de exhibición ID 2 si no existen
INSERT IGNORE INTO `comandos` (`id_vehiculo`, `nombre`, `codigo`, `descripcion`, `activo`)
SELECT 2, nombre, codigo, descripcion, activo FROM `comandos` WHERE id_vehiculo = 1;

-- -----------------------------------------------------------------------------
-- 5. TABLA: asignaciones_vehiculo
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `asignaciones_vehiculo` (
  `id_asignacion` INT NOT NULL AUTO_INCREMENT,
  `id_usuario` INT NOT NULL,
  `id_vehiculo` INT NOT NULL,
  `fecha_asignacion` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `estado` VARCHAR(20) NOT NULL DEFAULT 'ACTIVA',
  `autoriza_soporte` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id_asignacion`),
  UNIQUE KEY `uq_usuario_vehiculo_activo` (`id_vehiculo`, `estado`),
  KEY `fk_asig_usuario` (`id_usuario`),
  KEY `fk_asig_vehiculo` (`id_vehiculo`),
  CONSTRAINT `fk_asig_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_asig_vehiculo` FOREIGN KEY (`id_vehiculo`) REFERENCES `vehiculos` (`id_vehiculo`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Asignar el vehículo 1 al comprador Emmanuel González Mayorga
INSERT IGNORE INTO `asignaciones_vehiculo` (`id_usuario`, `id_vehiculo`, `estado`, `autoriza_soporte`)
VALUES (2, 1, 'ACTIVA', 0);

-- -----------------------------------------------------------------------------
-- 6. AMPLIACIÓN NO DESTRUCTIVA: demos
-- -----------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `_sp_migrar_demos_v2`;
DELIMITER ;;
CREATE PROCEDURE `_sp_migrar_demos_v2`()
BEGIN
    IF NOT EXISTS (
        SELECT * FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'demos' AND COLUMN_NAME = 'id_usuario_creador'
    ) THEN
        ALTER TABLE `demos` ADD COLUMN `id_usuario_creador` INT NULL AFTER `id_vehiculo`;
        ALTER TABLE `demos` ADD CONSTRAINT `fk_demo_creador` FOREIGN KEY (`id_usuario_creador`) REFERENCES `usuarios` (`id_usuario`) ON DELETE SET NULL ON UPDATE CASCADE;
    END IF;

    IF NOT EXISTS (
        SELECT * FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'demos' AND COLUMN_NAME = 'es_fabrica'
    ) THEN
        ALTER TABLE `demos` ADD COLUMN `es_fabrica` TINYINT(1) NOT NULL DEFAULT 1 AFTER `id_usuario_creador`;
    END IF;
END ;;
DELIMITER ;

CALL `_sp_migrar_demos_v2`();
DROP PROCEDURE IF EXISTS `_sp_migrar_demos_v2`;

UPDATE `demos` SET `es_fabrica` = 1 WHERE `es_fabrica` IS NULL;

-- -----------------------------------------------------------------------------
-- 7. TABLA: sesiones_invitado
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `sesiones_invitado` (
  `id_sesion` INT NOT NULL AUTO_INCREMENT,
  `id_usuario_invitado` INT NOT NULL,
  `id_vehiculo` INT NOT NULL,
  `inicio` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `fin_programado` TIMESTAMP NOT NULL,
  `token_sesion` VARCHAR(64) NOT NULL UNIQUE,
  `estado` VARCHAR(20) NOT NULL DEFAULT 'ACTIVA',
  PRIMARY KEY (`id_sesion`),
  KEY `fk_sesion_invitado` (`id_usuario_invitado`),
  KEY `fk_sesion_vehiculo` (`id_vehiculo`),
  CONSTRAINT `fk_sesion_invitado` FOREIGN KEY (`id_usuario_invitado`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_sesion_vehiculo` FOREIGN KEY (`id_vehiculo`) REFERENCES `vehiculos` (`id_vehiculo`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- -----------------------------------------------------------------------------
-- 8. TABLA: bitacora_auditoria
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `bitacora_auditoria` (
  `id_bitacora` BIGINT NOT NULL AUTO_INCREMENT,
  `id_usuario` INT NULL,
  `accion` VARCHAR(60) NOT NULL,
  `entidad_afectada` VARCHAR(60) NOT NULL,
  `id_entidad` INT NULL,
  `detalle_json` TEXT NULL,
  `ip_origen` VARCHAR(45) NULL,
  `fecha_hora` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_bitacora`),
  KEY `fk_bitacora_usuario` (`id_usuario`),
  CONSTRAINT `fk_bitacora_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Registrar evento de auditoría inicial
INSERT INTO `bitacora_auditoria` (`id_usuario`, `accion`, `entidad_afectada`, `id_entidad`, `detalle_json`, `ip_origen`)
VALUES (1, 'SISTEMA_INICIALIZADO', 'MIGRACION_V2', 2, '{"descripcion": "Migración V2 de Administración y RBAC ejecutada exitosamente"}', '127.0.0.1');
