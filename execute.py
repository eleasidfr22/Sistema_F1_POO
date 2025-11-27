# execute.py
# El punto de entrada principal debe usar importaciones directas para archivos en la raíz
# y usar el nombre del paquete (src) para las clases internas.

from conexion_db import ConexionDB
# Importación correcta: Usa 'src' porque es un paquete de carpetas
from src.vehiculos import AutoDeFormula1 


def probar_funcionalidad_inicial():
    """Prueba la conexión a la BD y los principios POO (Herencia/Polimorfismo)."""
    
    print("--- 🏁 PRUEBA DE CONEXIÓN A BASE DE DATOS ---")
    
    db = ConexionDB()
    conexion = db.conectar()

    if conexion:
        print("\n✅ Conexión a la base de datos verificada y funcionando.")
    else:
        # Nota: Si falla, revisa el archivo .env y que MySQL esté corriendo.
        print("\n❌ Error: La conexión a la base de datos falló. Revisa tu archivo .env y el servidor MySQL.")
    
    if conexion and conexion.is_connected():
        db.desconectar()
        
    print("-" * 50)
    print("--- 🏎️ PRUEBA DE PRINCIPIOS POO ---")

    # Demostración de Herencia y Polimorfismo
    auto_f1 = AutoDeFormula1(
        marca="Mercedes", 
        modelo="W16", 
        velocidad_maxima=360.0, 
        combustible=100.0, 
        nivel_aerodinamica=9.0
    )
    
    print(f"Objeto creado: {auto_f1.get_marca()} {auto_f1.get_modelo()}")
    print(f"Probando Polimorfismo: {auto_f1.acelerar()}")
    print("-" * 50)


if __name__ == "__main__":
    probar_funcionalidad_inicial()