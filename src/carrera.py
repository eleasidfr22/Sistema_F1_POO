# src/carrera.py
import sys
sys.path.append('..')
from conexion_db import get_conn
from datetime import datetime

class Carrera:
    """Clase que representa una carrera de F1"""
    
    def __init__(self, id_carrera, nombre, fecha, vueltas, clima, id_circuito):
        self._id_carrera = id_carrera
        self._nombre = nombre
        self._fecha = fecha
        self._vueltas = vueltas
        self._clima = clima
        self._id_circuito = id_circuito
    
    # Getters y Setters
    @property
    def id_carrera(self):
        return self._id_carrera
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor
    
    @property
    def fecha(self):
        return self._fecha
    
    @fecha.setter
    def fecha(self, valor):
        self._fecha = valor
    
    @property
    def vueltas(self):
        return self._vueltas
    
    @vueltas.setter
    def vueltas(self, valor):
        if valor > 0:
            self._vueltas = valor
    
    @property
    def clima(self):
        return self._clima
    
    @clima.setter
    def clima(self, valor):
        self._clima = valor
    
    @property
    def id_circuito(self):
        return self._id_circuito
    
    @id_circuito.setter
    def id_circuito(self, valor):
        self._id_circuito = valor
    
    # Métodos
    def iniciar_carrera(self):
        """Inicia la carrera"""
        return f"Iniciando {self._nombre} con {self._vueltas} vueltas. Clima: {self._clima}"
    
    def registrar_resultado(self, id_piloto, posicion, tiempo_total, puntos_obtenidos):
        """Registra el resultado de un piloto en la carrera"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Resultados (id_carrera, id_piloto, posicion, tiempo_total, puntos_obtenidos)
                VALUES (%s, %s, %s, %s, %s)
            """, (self._id_carrera, id_piloto, posicion, tiempo_total, puntos_obtenidos))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()
    
    def mostrar_resultados(self):
        """Muestra los resultados de la carrera"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT r.posicion, p.nombre, r.tiempo_total, r.puntos_obtenidos
                FROM Resultados r
                JOIN Pilotos p ON r.id_piloto = p.id_piloto
                WHERE r.id_carrera = %s
                ORDER BY r.posicion
            """, (self._id_carrera,))
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()
    
    # ==================== CRUD ====================
    
    @classmethod
    def crear(cls, nombre, fecha, vueltas, clima, id_circuito):
        """Crea una nueva carrera en la BD"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Carreras (nombre, fecha, vueltas, clima, id_circuito)
                VALUES (%s, %s, %s, %s, %s)
            """, (nombre, fecha, vueltas, clima, id_circuito))
            conn.commit()
            carrera_id = cur.lastrowid
            return cls(carrera_id, nombre, fecha, vueltas, clima, id_circuito)
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def listar_todas(cls):
        """Lista todas las carreras"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id_carrera, nombre, fecha, vueltas, clima, id_circuito
                FROM Carreras
                ORDER BY fecha DESC
            """)
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows]
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def buscar_por_id(cls, id_carrera):
        """Busca una carrera por ID"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id_carrera, nombre, fecha, vueltas, clima, id_circuito
                FROM Carreras
                WHERE id_carrera = %s
            """, (id_carrera,))
            r = cur.fetchone()
            return cls(r[0], r[1], r[2], r[3], r[4], r[5]) if r else None
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def buscar_por_nombre(cls, nombre):
        """Busca una carrera por nombre"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id_carrera, nombre, fecha, vueltas, clima, id_circuito
                FROM Carreras
                WHERE nombre = %s
            """, (nombre,))
            r = cur.fetchone()
            return cls(r[0], r[1], r[2], r[3], r[4], r[5]) if r else None
        finally:
            cur.close()
            conn.close()
    
    def __str__(self):
        return f"{self._nombre} ({self._fecha}) - {self._vueltas} vueltas"