-- ========================================
-- SISTEMA DE GESTIÓN DE CARRERAS F1
-- Script de creación de base de datos
-- ========================================

-- Seleccionar/Crear base de datos
CREATE DATABASE IF NOT EXISTS sistemaf1db;
USE sistemaf1db;

-- ========================================
-- 1. TABLA CIRCUITOS
-- ========================================
CREATE TABLE IF NOT EXISTS Circuitos (
    id_circuito INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    pais VARCHAR(50) NOT NULL,
    longitud DECIMAL(5, 3) NOT NULL,
    numeroCurvas INT DEFAULT 0
) ENGINE=InnoDB;

-- ========================================
-- 2. TABLA EQUIPOS (CRUD Requerido)
-- ========================================
CREATE TABLE IF NOT EXISTS Equipos (
    id_equipo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    pais VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

-- ========================================
-- 3. TABLA AUTOSF1 (Relacionada con Equipos)
-- ========================================
CREATE TABLE IF NOT EXISTS AutosF1 (
    id_auto INT AUTO_INCREMENT PRIMARY KEY,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    velocidadMaxima DECIMAL(5, 2) DEFAULT 0.00,
    combustible DECIMAL(5, 2) DEFAULT 100.00,
    nivelAerodinamica DECIMAL(4, 2) NOT NULL,
    modoDRS BOOLEAN DEFAULT FALSE,
    id_equipo INT,
    FOREIGN KEY (id_equipo) REFERENCES Equipos(id_equipo) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ========================================
-- 4. TABLA PILOTOS (CRUD Requerido, Relacionada con Equipos)
-- ========================================
CREATE TABLE IF NOT EXISTS Pilotos (
    id_piloto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    nacionalidad VARCHAR(50),
    experiencia INT DEFAULT 1,
    puntos DECIMAL(6, 2) DEFAULT 0.00,
    id_equipo INT,
    FOREIGN KEY (id_equipo) REFERENCES Equipos(id_equipo) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ========================================
-- 5. TABLA CARRERAS (Relacionada con Circuitos)
-- ========================================
CREATE TABLE IF NOT EXISTS Carreras (
    id_carrera INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha DATE,
    vueltas INT DEFAULT 50,
    clima VARCHAR(50) DEFAULT 'Soleado',
    id_circuito INT,
    FOREIGN KEY (id_circuito) REFERENCES Circuitos(id_circuito) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ========================================
-- 6. TABLA RESULTADOS (Relaciona Carreras y Pilotos)
-- ========================================
CREATE TABLE IF NOT EXISTS Resultados (
    id_resultado INT AUTO_INCREMENT PRIMARY KEY,
    id_carrera INT NOT NULL,
    id_piloto INT NOT NULL,
    posicion INT NOT NULL,
    tiempo_total TIME,
    puntos_obtenidos DECIMAL(4, 2) DEFAULT 0.00,
    FOREIGN KEY (id_carrera) REFERENCES Carreras(id_carrera) ON DELETE CASCADE,
    FOREIGN KEY (id_piloto) REFERENCES Pilotos(id_piloto) ON DELETE CASCADE,
    UNIQUE(id_carrera, id_piloto)
) ENGINE=InnoDB;

-- ========================================
-- 7. TABLA MECANICOS (Opcional, Relacionada con Equipos)
-- ========================================
CREATE TABLE IF NOT EXISTS Mecanicos (
    id_mecanico INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100) NOT NULL,
    experiencia INT DEFAULT 1,
    id_equipo INT,
    FOREIGN KEY (id_equipo) REFERENCES Equipos(id_equipo) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ========================================
-- VERIFICAR TABLAS CREADAS
-- ========================================
SHOW TABLES;