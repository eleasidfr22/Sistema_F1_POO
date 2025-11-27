# src/auto.py
class Auto:
    """Clase base que representa un vehículo de competencia"""
    
    def __init__(self, marca, modelo, velocidad_maxima, combustible):
        self._marca = marca
        self._modelo = modelo
        self._velocidad_maxima = velocidad_maxima
        self._combustible = combustible
    
    # Getters y Setters (Encapsulamiento)
    @property
    def marca(self):
        return self._marca
    
    @marca.setter
    def marca(self, valor):
        self._marca = valor
    
    @property
    def modelo(self):
        return self._modelo
    
    @modelo.setter
    def modelo(self, valor):
        self._modelo = valor
    
    @property
    def velocidad_maxima(self):
        return self._velocidad_maxima
    
    @velocidad_maxima.setter
    def velocidad_maxima(self, valor):
        if valor > 0:
            self._velocidad_maxima = valor
    
    @property
    def combustible(self):
        return self._combustible
    
    @combustible.setter
    def combustible(self, valor):
        if 0 <= valor <= 100:
            self._combustible = valor
    
    # Métodos
    def acelerar(self):
        """Aumenta la velocidad del auto"""
        if self._combustible > 0:
            self._combustible -= 0.5
            return f"{self._marca} {self._modelo} acelera. Combustible: {self._combustible}%"
        return "Sin combustible"
    
    def frenar(self):
        """Reduce la velocidad del auto"""
        return f"{self._marca} {self._modelo} está frenando"
    
    def mostrar_info(self):
        """Muestra información del auto"""
        return f"Auto: {self._marca} {self._modelo} - Vel. Max: {self._velocidad_maxima} km/h - Combustible: {self._combustible}%"