class Auto:
    """Clase base que representa un vehículo de competencia general."""
    def __init__(self, marca: str, modelo: str, velocidad_maxima: float, combustible: float):
        # Encapsulamiento: Atributos privados
        self.__marca = marca
        self.__modelo = modelo
        self.__velocidad_maxima = velocidad_maxima
        self.__combustible = combustible

    # Getters necesarios para Polimorfismo/otras clases
    def get_marca(self):
        return self.__marca
    
    def get_modelo(self):
        return self.__modelo
    
    def get_velocidad_maxima(self):
        return self.__velocidad_maxima
    
    def get_combustible(self):
        return self.__combustible
    
    # Setter necesario para el consumo
    def set_combustible(self, cantidad: float):
        if cantidad >= 0:
            self.__combustible = cantidad
    
    # Método base para Polimorfismo
    def acelerar(self):
        """Método base para acelerar (consumo estándar)."""
        if self.__combustible >= 1.0:
            self.set_combustible(self.__combustible - 1.0)
            return f"El {self.__marca} está acelerando con velocidad estándar."
        else:
            return "Sin combustible."

class AutoDeFormula1(Auto):
    """Clase que hereda de Auto, con características de F1 (DRS, Aerodinámica)."""
    def __init__(self, marca: str, modelo: str, velocidad_maxima: float, combustible: float, nivel_aerodinamica: float, modo_drs: bool = False):
        # Herencia: Llama al constructor de la clase base Auto
        super().__init__(marca, modelo, velocidad_maxima, combustible)
        
        self.__nivel_aerodinamica = nivel_aerodinamica
        self.__modo_drs = modo_drs
        self.__energia_ers = 100.0 # Energía Eléctrica para la simulación

    def calcularRendimiento(self):
        """Método para calcular el rendimiento específico de F1."""
        rendimiento = self.__nivel_aerodinamica * 0.5 + self.__energia_ers * 0.2
        return rendimiento

    # Polimorfismo: Sobrescribe el método acelerar() de la clase base
    def acelerar(self):
        """Aceleración avanzada que considera factores adicionales (aerodinámica, ERS)."""
        mensaje_base = super().acelerar()
        if "acelerando" in mensaje_base:
            rendimiento_extra = self.calcularRendimiento() / 100
            # Consumo extra por el alto rendimiento
            self.set_combustible(self.get_combustible() - 0.5) 
            self.__energia_ers -= 1.0 
            return f"{mensaje_base} (Potencia F1: +{rendimiento_extra:.2f} extra). ERS restante: {self.__energia_ers:.1f}"
        return mensaje_base