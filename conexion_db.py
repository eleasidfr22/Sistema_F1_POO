# conexion_db.py
import mysql.connector
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
# Este comando busca el archivo .env en la raíz del proyecto y carga las variables
load_dotenv()

class ConexionDB:
    """Clase para manejar la conexión y operaciones de BD (demuestra Encapsulamiento)."""

    def __init__(self):
        # Atributos encapsulados (privados) que cargan la configuración desde el .env
        self.__host = os.getenv("DB_HOST")
        self.__user = os.getenv("DB_USER")
        self.__password = os.getenv("DB_PASSWORD")
        self.__database = os.getenv("DB_DATABASE",) # sistema_f1_db
        self.__connection = None

    def conectar(self):
        """Establece la conexión a la base de datos."""
        try:
            self.__connection = mysql.connector.connect(
                host=self.__host,
                user=self.__user,
                password=self.__password,
                database=self.__database
            )
            # Retorna la conexión si es exitosa
            return self.__connection
        except mysql.connector.Error as err:
            # Puedes imprimir el error de conexión para depuración
            # print(f"Error de conexión a MySQL: {err}")
            return None

    def desconectar(self):
        """Cierra la conexión si está abierta."""
        if self.__connection and self.__connection.is_connected():
            self.__connection.close()

    def ejecutar_dml(self, query, params=None):
        """
        Método genérico para ejecutar consultas DML (Data Manipulation Language: 
        INSERT, UPDATE, DELETE) y asegurar el manejo de la conexión.
        """
        conn = self.conectar()
        row_count = 0
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, params or ())
                conn.commit()
                row_count = cursor.rowcount # Número de filas afectadas
            except mysql.connector.Error as err:
                print(f"Error al ejecutar DML: {err}")
                conn.rollback() # Deshace los cambios en caso de error
            finally:
                cursor.close()
                self.desconectar() # Asegura que la conexión siempre se cierre
        return row_count