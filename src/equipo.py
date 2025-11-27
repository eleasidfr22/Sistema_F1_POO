# src/equipo.py
import sys
sys.path.append('..')
from conexion_db import get_conn

class Equipo:
    """Clase que representa una escudería de F1"""
    
    def __init__(self, id_equipo, nombre, pais):
        self._id_equipo = id_equipo
        self._nombre = nombre
        self._pais = pais
    
    # Getters y Setters
    @property
    def id_equipo(self):
        return self._id_equipo
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor
    
    @property
    def pais(self):
        return self._pais
    
    @pais.setter
    def pais(self, valor):
        self._pais = valor
    
    # Métodos
    def mostrar_equipo(self):
        """Muestra información del equipo"""
        return f"[{self._id_equipo}] {self._nombre} ({self._pais})"
    
    def obtener_pilotos(self):
        """Obtiene los pilotos del equipo"""
        from src.piloto import Piloto
        return Piloto.buscar_por_equipo(self._id_equipo)
    
    def obtener_autos(self):
        """Obtiene los autos del equipo"""
        from src.auto_formula1 import AutoDeFormula1
        return AutoDeFormula1.buscar_por_equipo(self._id_equipo)
    
    # ==================== CRUD ====================
    
    @classmethod
    def crear(cls, nombre, pais):
        """Crea un nuevo equipo en la BD"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Equipos (nombre, pais)
                VALUES (%s, %s)
            """, (nombre, pais))
            conn.commit()
            equipo_id = cur.lastrowid
            return cls(equipo_id, nombre, pais)
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def listar_todos(cls):
        """Lista todos los equipos"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id_equipo, nombre, pais
                FROM Equipos
                ORDER BY nombre
            """)
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2]) for r in rows]
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def buscar_por_id(cls, id_equipo):
        """Busca un equipo por ID"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id_equipo, nombre, pais
                FROM Equipos
                WHERE id_equipo = %s
            """, (id_equipo,))
            r = cur.fetchone()
            return cls(r[0], r[1], r[2]) if r else None
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def buscar_por_nombre(cls, nombre):
        """Busca un equipo por nombre"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id_equipo, nombre, pais
                FROM Equipos
                WHERE nombre = %s
            """, (nombre,))
            r = cur.fetchone()
            return cls(r[0], r[1], r[2]) if r else None
        finally:
            cur.close()
            conn.close()
    
    def __str__(self):
        return f"{self._nombre} ({self._pais})"