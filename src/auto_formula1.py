# src/auto_formula1.py
import sys
sys.path.append('..')
from conexion_db import get_conn
from src.auto import Auto

class AutoDeFormula1(Auto):
    """Clase que representa un auto de Fórmula 1 con CRUD integrado"""
    
    def __init__(self, id_auto, marca, modelo, velocidad_maxima, combustible, 
                 nivel_aerodinamica, modo_drs, id_equipo=None):
        super().__init__(marca, modelo, velocidad_maxima, combustible)
        self._id_auto = id_auto
        self._nivel_aerodinamica = nivel_aerodinamica
        self._modo_drs = modo_drs
        self._id_equipo = id_equipo
    
    @property
    def id_auto(self):
        return self._id_auto
    
    @property
    def nivel_aerodinamica(self):
        return self._nivel_aerodinamica
    
    @nivel_aerodinamica.setter
    def nivel_aerodinamica(self, valor):
        if 0 <= valor <= 10:
            self._nivel_aerodinamica = valor
    
    @property
    def modo_drs(self):
        return self._modo_drs
    
    @modo_drs.setter
    def modo_drs(self, valor):
        self._modo_drs = valor
    
    @property
    def id_equipo(self):
        return self._id_equipo
    
    @id_equipo.setter
    def id_equipo(self, valor):
        self._id_equipo = valor
    
    # Polimorfismo: sobrescribe el método acelerar
    def acelerar(self):
        """Acelerar considerando aerodinámica y DRS"""
        if self._combustible > 0:
            consumo = 0.3 if self._modo_drs else 0.5
            self._combustible -= consumo
            velocidad_boost = self._nivel_aerodinamica * 10
            return f"F1 {self._marca} acelera con DRS={'ON' if self._modo_drs else 'OFF'}. Boost: +{velocidad_boost} km/h"
        return "Sin combustible"
    
    def activar_drs(self):
        self._modo_drs = True
        return "DRS activado"
    
    def desactivar_drs(self):
        self._modo_drs = False
        return "DRS desactivado"
    
    def calcular_rendimiento(self):
        """Calcula el rendimiento del auto"""
        rendimiento = (self._velocidad_maxima * 0.4) + (self._nivel_aerodinamica * 10) + (self._combustible * 0.5)
        return round(rendimiento, 2)
    
    def mostrar_info(self):
        """Sobrescribe mostrar_info para incluir datos de F1"""
        return (f"[{self._id_auto}] {self._marca} {self._modelo} | "
                f"Vel.Max: {self._velocidad_maxima} km/h | "
                f"Aero: {self._nivel_aerodinamica} | "
                f"DRS: {'Sí' if self._modo_drs else 'No'}")
    
    # ==================== CRUD (estilo biblioteca) ====================
    
    @classmethod
    def crear(cls, marca, modelo, velocidad_maxima, combustible, nivel_aerodinamica, modo_drs, id_equipo):
        """Crea un nuevo auto F1 en la BD"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO AutosF1 (marca, modelo, velocidadMaxima, combustible, nivelAerodinamica, modoDRS, id_equipo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (marca, modelo, velocidad_maxima, combustible, nivel_aerodinamica, modo_drs, id_equipo))
            conn.commit()
            auto_id = cur.lastrowid
            return cls(auto_id, marca, modelo, velocidad_maxima, combustible, nivel_aerodinamica, modo_drs, id_equipo)
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def listar_todos(cls):
        """Lista todos los autos F1"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id_auto, marca, modelo, velocidadMaxima, combustible, 
                       nivelAerodinamica, modoDRS, id_equipo
                FROM AutosF1
                ORDER BY marca, modelo
            """)
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2], r[3], r[4], r[5], bool(r[6]), r[7]) for r in rows]
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def buscar_por_id(cls, id_auto):
        """Busca un auto por ID"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id_auto, marca, modelo, velocidadMaxima, combustible,
                       nivelAerodinamica, modoDRS, id_equipo
                FROM AutosF1
                WHERE id_auto = %s
            """, (id_auto,))
            r = cur.fetchone()
            return cls(r[0], r[1], r[2], r[3], r[4], r[5], bool(r[6]), r[7]) if r else None
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def buscar_por_equipo(cls, id_equipo):
        """Busca autos de un equipo específico"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id_auto, marca, modelo, velocidadMaxima, combustible,
                       nivelAerodinamica, modoDRS, id_equipo
                FROM AutosF1
                WHERE id_equipo = %s
            """, (id_equipo,))
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2], r[3], r[4], r[5], bool(r[6]), r[7]) for r in rows]
        finally:
            cur.close()
            conn.close()
    
    def __str__(self):
        return f"{self._marca} {self._modelo} (Equipo ID: {self._id_equipo})"