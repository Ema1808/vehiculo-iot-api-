-- =============================================================================
-- MIGRACIÓN V2: MÓDULO DE ADMINISTRACIÓN IoT + RBAC + ASIGNACIONES + AUDITORÍA
-- Base de datos: vehiculo_iot (Amazon RDS MySQL)
-- Script: DOWN (Reversión limpia para entornos de prueba)
-- =============================================================================

USE `vehiculo_iot`;

-- 1. Eliminar bitácora
DROP TABLE IF EXISTS `bitacora_auditoria`;

-- 2. Eliminar sesiones de invitados
DROP TABLE IF EXISTS `sesiones_invitado`;

-- 3. Revertir columnas de demos
DROP PROCEDURE IF EXISTS `_sp_revertir_demos_v2`;
DELIMITER ;;
CREATE PROCEDURE `_sp_revertir_demos_v2`()
BEGIN
    IF EXISTS (
        SELECT * FROM information_schema.TABLE_CONSTRAINTS 
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'demos' AND CONSTRAINT_NAME = 'fk_demo_creador'
    ) THEN
        ALTER TABLE `demos` DROP FOREIGN KEY `fk_demo_creador`;
    END IF;

    IF EXISTS (
        SELECT * FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'demos' AND COLUMN_NAME = 'id_usuario_creador'
    ) THEN
        ALTER TABLE `demos` DROP COLUMN `id_usuario_creador`;
    END IF;

    IF EXISTS (
        SELECT * FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'demos' AND COLUMN_NAME = 'es_fabrica'
    ) THEN
        ALTER TABLE `demos` DROP COLUMN `es_fabrica`;
    END IF;
END ;;
DELIMITER ;
CALL `_sp_revertir_demos_v2`();
DROP PROCEDURE IF EXISTS `_sp_revertir_demos_v2`;

-- 4. Eliminar asignaciones
DROP TABLE IF EXISTS `asignaciones_vehiculo`;

-- 5. Eliminar unidad demo 2 si fue creada
DELETE FROM `comandos` WHERE `id_vehiculo` = 2;
DELETE FROM `vehiculos` WHERE `id_vehiculo` = 2;

-- 6. Revertir columnas de vehiculos
DROP PROCEDURE IF EXISTS `_sp_revertir_vehiculos_v2`;
DELIMITER ;;
CREATE PROCEDURE `_sp_revertir_vehiculos_v2`()
BEGIN
    IF EXISTS (
        SELECT * FROM information_schema.TABLE_CONSTRAINTS 
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'vehiculos' AND CONSTRAINT_NAME = 'fk_vehiculo_modelo'
    ) THEN
        ALTER TABLE `vehiculos` DROP FOREIGN KEY `fk_vehiculo_modelo`;
    END IF;

    IF EXISTS (
        SELECT * FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'vehiculos' AND COLUMN_NAME = 'id_modelo'
    ) THEN
        ALTER TABLE `vehiculos` DROP COLUMN `id_modelo`;
    END IF;

    IF EXISTS (
        SELECT * FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'vehiculos' AND COLUMN_NAME = 'numero_serie'
    ) THEN
        ALTER TABLE `vehiculos` DROP COLUMN `numero_serie`;
    END IF;

    IF EXISTS (
        SELECT * FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'vehiculos' AND COLUMN_NAME = 'estado_comercial'
    ) THEN
        ALTER TABLE `vehiculos` DROP COLUMN `estado_comercial`;
    END IF;
END ;;
DELIMITER ;
CALL `_sp_revertir_vehiculos_v2`();
DROP PROCEDURE IF EXISTS `_sp_revertir_vehiculos_v2`;

-- 7. Eliminar modelos
DROP TABLE IF EXISTS `modelos_vehiculo`;

-- 8. Eliminar usuarios
DROP TABLE IF EXISTS `usuarios`;

-- 9. Eliminar roles
DROP TABLE IF EXISTS `roles`;
