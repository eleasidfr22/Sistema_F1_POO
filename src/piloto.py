# src/piloto.py
import sys
sys.path.append('..')
from conexion_db import get_conn

class Piloto:
    """Clase que representa un piloto de F1"""
    
    def __init__(self, id_piloto, nombre, nacionalidad, experiencia, puntos, id_equipo=None):
        self._id_piloto = id_piloto
        self._nombre = nombre
        self._nacionalidad = nacionalidad
        self._experiencia = experiencia
        self._puntos = puntos
        self._id_equipo = id_equipo
    
    # Getters y Setters (Encapsulamiento)
    @property
    def id_piloto(self):
        return self._id_piloto
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor
    
    @property
    def nacionalidad(self):
        return self._nacionalidad
    
    @nacionalidad.setter
    def nacionalidad(self, valor):
        self._nacionalidad = valor
    
    @property
    def experiencia(self):
        return self._experiencia
    
    @experiencia.setter
    def experiencia(self, valor):
        if valor >= 0:
            self._experiencia = valor
    
    @property
    def puntos(self):
        return self._puntos
    
    @puntos.setter
    def puntos(self, valor):
        if valor >= 0:
            self._puntos = valor
    
    @property
    def id_equipo(self):
        return self._id_equipo
    
    @id_equipo.setter
    def id_equipo(self, valor):
        self._id_equipo = valor
    
    # Métodos
    def participar_carrera(self):
        """Simula la participación del piloto en una carrera"""
        return f"{self._nombre} está participando en la carrera"
    
    def obtener_puntos(self, puntos_nuevos):
        """Suma puntos al piloto"""
        self._puntos += puntos_nuevos
        return f"{self._nombre} ahora tiene {self._puntos} puntos"
    
    def mostrar_estadisticas(self):
        """Muestra las estadísticas del piloto"""
        return (f"[{self._id_piloto}] {self._nombre} ({self._nacionalidad}) | "
                f"Experiencia: {self._experiencia} años | Puntos: {self._puntos}")
    
    # ==================== CRUD ====================
    
    @classmethod
    def crear(cls, nombre, nacionalidad, experiencia, puntos, id_equipo=None):
        """Crea un nuevo piloto en la BD"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Pilotos (nombre, nacionalidad, experiencia, puntos, id_equipo)
                VALUES (%s, %s, %s, %s, %s)
            """, (nombre, nacionalidad, experiencia, puntos, id_equipo))
            conn.commit()
            piloto_id = cur.lastrowid
            return cls(piloto_id, nombre, nacionalidad, experiencia, puntos, id_equipo)
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def listar_todos(cls):
        """Lista todos los pilotos"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id_piloto, nombre, nacionalidad, experiencia, puntos, id_equipo
                FROM Pilotos
                ORDER BY puntos DESC, nombre
            """)
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows]
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def buscar_por_id(cls, id_piloto):
        """Busca un piloto por ID"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id_piloto, nombre, nacionalidad, experiencia, puntos, id_equipo
                FROM Pilotos
                WHERE id_piloto = %s
            """, (id_piloto,))
            r = cur.fetchone()
            return cls(r[0], r[1], r[2], r[3], r[4], r[5]) if r else None
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def buscar_por_nombre(cls, nombre):
        """Busca un piloto por nombre"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id_piloto, nombre, nacionalidad, experiencia, puntos, id_equipo
                FROM Pilotos
                WHERE nombre = %s
            """, (nombre,))
            r = cur.fetchone()
            return cls(r[0], r[1], r[2], r[3], r[4], r[5]) if r else None
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def buscar_por_equipo(cls, id_equipo):
        """Busca pilotos de un equipo específico"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id_piloto, nombre, nacionalidad, experiencia, puntos, id_equipo
                FROM Pilotos
                WHERE id_equipo = %s
            """, (id_equipo,))
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows]
        finally:
            cur.close()
            conn.close()
    
    def actualizar_puntos(self):
        """Actualiza los puntos del piloto en la BD"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE Pilotos SET puntos = %s WHERE id_piloto = %s
            """, (self._puntos, self._id_piloto))
            conn.commit()
        finally:
            cur.close()
            conn.close()
    
    def __str__(self):
        return f"{self._nombre} ({self._nacionalidad}) - {self._puntos} pts"