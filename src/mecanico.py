# src/mecanico.py
import sys
sys.path.append('..')
from conexion_db import get_conn

class Mecanico:
    """Clase que representa un mecánico de F1"""
    
    def __init__(self, id_mecanico, nombre, especialidad, experiencia, id_equipo=None):
        self._id_mecanico = id_mecanico
        self._nombre = nombre
        self._especialidad = especialidad
        self._experiencia = experiencia
        self._id_equipo = id_equipo
    
    # Getters y Setters
    @property
    def id_mecanico(self):
        return self._id_mecanico
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor
    
    @property
    def especialidad(self):
        return self._especialidad
    
    @especialidad.setter
    def especialidad(self, valor):
        self._especialidad = valor
    
    @property
    def experiencia(self):
        return self._experiencia
    
    @experiencia.setter
    def experiencia(self, valor):
        if valor >= 0:
            self._experiencia = valor
    
    @property
    def id_equipo(self):
        return self._id_equipo
    
    @id_equipo.setter
    def id_equipo(self, valor):
        self._id_equipo = valor
    
    # Métodos
    def revisar_auto(self, auto):
        """Revisa el estado de un auto"""
        return f"{self._nombre} está revisando el auto {auto.marca} {auto.modelo}"
    
    def reparar_auto(self, auto):
        """Repara un auto"""
        return f"{self._nombre} ha reparado el auto {auto.marca} {auto.modelo}"
    
    def mostrar_informacion(self):
        """Muestra información del mecánico"""
        return (f"[{self._id_mecanico}] {self._nombre} | "
                f"Especialidad: {self._especialidad} | "
                f"Experiencia: {self._experiencia} años")
    
    # ==================== CRUD ====================
    
    @classmethod
    def crear(cls, nombre, especialidad, experiencia, id_equipo=None):
        """Crea un nuevo mecánico en la BD"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Mecanicos (nombre, especialidad, experiencia, id_equipo)
                VALUES (%s, %s, %s, %s)
            """, (nombre, especialidad, experiencia, id_equipo))
            conn.commit()
            mecanico_id = cur.lastrowid
            return cls(mecanico_id, nombre, especialidad, experiencia, id_equipo)
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def listar_todos(cls):
        """Lista todos los mecánicos"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id_mecanico, nombre, especialidad, experiencia, id_equipo
                FROM Mecanicos
                ORDER BY nombre
            """)
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2], r[3], r[4]) for r in rows]
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def buscar_por_equipo(cls, id_equipo):
        """Busca mecánicos de un equipo específico"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id_mecanico, nombre, especialidad, experiencia, id_equipo
                FROM Mecanicos
                WHERE id_equipo = %s
            """, (id_equipo,))
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2], r[3], r[4]) for r in rows]
        finally:
            cur.close()
            conn.close()
    
    def __str__(self):
        return f"{self._nombre} - {self._especialidad}"