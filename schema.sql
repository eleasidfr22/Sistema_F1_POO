USE sistemaf1db;

-- ========================================
-- MEJORAR TABLAS EXISTENTES
-- ========================================

-- 1. CIRCUITOS: Agregar número de curvas (según tu caso de estudio)
ALTER TABLE Circuitos 
ADD COLUMN numeroCurvas INT DEFAULT 0;

-- 2. AUTOSF1: Agregar campos del caso de estudio
ALTER TABLE AutosF1 
ADD COLUMN velocidadMaxima DECIMAL(5, 2) DEFAULT 0.00,
ADD COLUMN combustible DECIMAL(5, 2) DEFAULT 100.00,
ADD COLUMN modoDRS BOOLEAN DEFAULT FALSE;

-- 3. CARRERAS: Agregar campos importantes
ALTER TABLE Carreras 
ADD COLUMN vueltas INT DEFAULT 50,
ADD COLUMN clima VARCHAR(50) DEFAULT 'Soleado';

-- ========================================
-- TABLA NUEVA: RESULTADOS (¡IMPORTANTE!)
-- ========================================
-- Esta tabla es CLAVE para relacionar Pilotos con Carreras
-- y registrar los resultados de cada competencia

CREATE TABLE Resultados (
    id_resultado INT AUTO_INCREMENT PRIMARY KEY,
    id_carrera INT NOT NULL,
    id_piloto INT NOT NULL,
    posicion INT NOT NULL,
    tiempo_total TIME,
    puntos_obtenidos DECIMAL(4, 2) DEFAULT 0.00,
    FOREIGN KEY (id_carrera) REFERENCES Carreras(id_carrera) ON DELETE CASCADE,
    FOREIGN KEY (id_piloto) REFERENCES Pilotos(id_piloto) ON DELETE CASCADE,
    UNIQUE(id_carrera, id_piloto) -- Un piloto no puede tener dos resultados en la misma carrera
);

-- ========================================
-- OPCIONAL: TABLA MECANICOS (Para tener 7 clases)
-- ========================================
CREATE TABLE Mecanicos (
    id_mecanico INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100) NOT NULL,
    experiencia INT DEFAULT 1,
    id_equipo INT,
    FOREIGN KEY (id_equipo) REFERENCES Equipos(id_equipo) ON DELETE SET NULL
);