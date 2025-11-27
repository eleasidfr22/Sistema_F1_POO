# src/circuito.py
import sys
sys.path.append('..')
from conexion_db import get_conn

class Circuito:
    """Clase que representa un circuito de F1"""
    
    def __init__(self, id_circuito, nombre, pais, longitud, numero_curvas):
        self._id_circuito = id_circuito
        self._nombre = nombre
        self._pais = pais
        self._longitud = longitud
        self._numero_curvas = numero_curvas
    
    # Getters y Setters
    @property
    def id_circuito(self):
        return self._id_circuito
    
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
    
    @property
    def longitud(self):
        return self._longitud
    
    @longitud.setter
    def longitud(self, valor):
        if valor > 0:
            self._longitud = valor
    
    @property
    def numero_curvas(self):
        return self._numero_curvas
    
    @numero_curvas.setter
    def numero_curvas(self, valor):
        if valor >= 0:
            self._numero_curvas = valor
    
    # Métodos
    def mostrar_datos_circuito(self):
        """Muestra información del circuito"""
        return (f"[{self._id_circuito}] {self._nombre} ({self._pais}) | "
                f"Longitud: {self._longitud} km | Curvas: {self._numero_curvas}")
    
    def obtener_condiciones(self):
        """Simula obtener condiciones del circuito"""
        return f"Condiciones del circuito {self._nombre}: Pista seca, temperatura 25°C"
    
    # ==================== CRUD ====================
    
    @classmethod
    def crear(cls, nombre, pais, longitud, numero_curvas):
        """Crea un nuevo circuito en la BD"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Circuitos (nombre, pais, longitud, numeroCurvas)
                VALUES (%s, %s, %s, %s)
            """, (nombre, pais, longitud, numero_curvas))
            conn.commit()
            circuito_id = cur.lastrowid
            return cls(circuito_id, nombre, pais, longitud, numero_curvas)
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def listar_todos(cls):
        """Lista todos los circuitos"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id_circuito, nombre, pais, longitud, numeroCurvas
                FROM Circuitos
                ORDER BY nombre
            """)
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2], r[3], r[4]) for r in rows]
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def buscar_por_id(cls, id_circuito):
        """Busca un circuito por ID"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id_circuito, nombre, pais, longitud, numeroCurvas
                FROM Circuitos
                WHERE id_circuito = %s
            """, (id_circuito,))
            r = cur.fetchone()
            return cls(r[0], r[1], r[2], r[3], r[4]) if r else None
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def buscar_por_nombre(cls, nombre):
        """Busca un circuito por nombre"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id_circuito, nombre, pais, longitud, numeroCurvas
                FROM Circuitos
                WHERE nombre = %s
            """, (nombre,))
            r = cur.fetchone()
            return cls(r[0], r[1], r[2], r[3], r[4]) if r else None
        finally:
            cur.close()
            conn.close()
    
    def __str__(self):
        return f"{self._nombre} ({self._pais}) - {self._longitud} km"