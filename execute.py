# execute.py
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from conexion_db import get_conn 

# Clases del sistema
from src.equipo import Equipo
from src.piloto import Piloto
from src.auto_formula1 import AutoDeFormula1
from src.carrera import Carrera
from src.circuito import Circuito
from src.mecanico import Mecanico

# Variables globales para el estado de la aplicación
CURRENT_USER_ROL = None
MAIN_WINDOW = None 
LOGIN_WINDOW = None
lb_output = None # Se inicializará en la función inicializar_interfaz_principal

# ====================================================================
# LÓGICA DE AUTENTICACIÓN
# ====================================================================

def verificar_credenciales(usuario, contrasena):
    """
    Consulta la DB para validar credenciales y obtener el rol.
    Retorna (True/False, rol)
    """
    conn = get_conn()
    if conn is None:
        messagebox.showerror("Error de Conexión", "No se pudo obtener una conexión a la base de datos.")
        return False, None
    
    cursor = conn.cursor()
    # Consulta la tabla 'Usuarios'
    query = "SELECT rol FROM Usuarios WHERE nombre_usuario = %s AND contrasena = %s"
    
    try:
        cursor.execute(query, (usuario, contrasena))
        resultado = cursor.fetchone()
        
        if resultado:
            rol_obtenido = resultado[0]
            return True, rol_obtenido 
        else:
            return False, None
            
    except Exception as e:
        messagebox.showerror("Error de SQL", f"Error al consultar usuarios: {e}")
        return False, None
        
    finally:
        if conn:
            cursor.close()
            conn.close() # Devuelve la conexión al pool

def intentar_iniciar_sesion(usuario_entry, contrasena_entry, login_win):
    """Maneja el evento del botón 'Iniciar Sesión'."""
    global CURRENT_USER_ROL, MAIN_WINDOW, LOGIN_WINDOW
    
    usuario = usuario_entry.get()
    contrasena = contrasena_entry.get() 
    
    # Limpiar campos inmediatamente
    usuario_entry.delete(0, tk.END)
    contrasena_entry.delete(0, tk.END)

    es_valido, rol = verificar_credenciales(usuario, contrasena)
    
    if es_valido:
        CURRENT_USER_ROL = rol
        login_win.destroy()
        LOGIN_WINDOW = None
        
        # 1. Crear y mostrar la ventana principal (root)
        MAIN_WINDOW = tk.Tk()
        MAIN_WINDOW.title(f"Sistema de Gestión F1 - Interfaz Gráfica ({rol.capitalize()})")
        MAIN_WINDOW.geometry("900x600")
        MAIN_WINDOW.minsize(800, 500)
        
        # 2. Inicializar la interfaz con el rol
        inicializar_interfaz_principal(MAIN_WINDOW, rol)
        
    else:
        messagebox.showerror("Error de Login", "Usuario o contraseña incorrectos.")

def mostrar_ventana_login():
    """Crea y muestra la ventana de inicio de sesión."""
    global LOGIN_WINDOW
    
    # Crea la ventana de login
    LOGIN_WINDOW = tk.Tk()
    LOGIN_WINDOW.title("Inicio de Sesión F1")
    
    # Manejo del cierre de ventana
    def on_closing():
        if messagebox.askokcancel("Salir", "¿Realmente quieres cerrar la aplicación?"):
            sys.exit(0)
            
    LOGIN_WINDOW.protocol("WM_DELETE_WINDOW", on_closing)

    frame = ttk.Frame(LOGIN_WINDOW, padding="20 20 20 20")
    frame.pack(fill='both', expand=True)

    tk.Label(frame, text="Usuario:", font=("Segoe UI", 12)).pack(pady=5)
    entry_usuario = tk.Entry(frame, width=30, font=("Segoe UI", 12))
    entry_usuario.pack(padx=10)
    
    tk.Label(frame, text="Contraseña:", font=("Segoe UI", 12)).pack(pady=5)
    entry_contrasena = tk.Entry(frame, width=30, show="*", font=("Segoe UI", 12))
    entry_contrasena.pack(padx=10)

    tk.Button(frame, text="Iniciar Sesión", font=("Segoe UI", 12, "bold"), 
              command=lambda: intentar_iniciar_sesion(entry_usuario, entry_contrasena, LOGIN_WINDOW)).pack(pady=20)
    
    tk.Label(frame, text="Roles de prueba: admin_f1/password_admin, usuario_f1/password_user", 
             font=("Segoe UI", 8), fg="gray").pack(pady=5)

    LOGIN_WINDOW.mainloop()

# ====================================================================
# FUNCIONES CRUD (MODIFICADAS PARA USAR get_conn y finally)
# ====================================================================

# FUNCIONES PARA EQUIPOS (CRUD)
def registrar_equipo():
    nombre = simpledialog.askstring("Registrar Equipo", "Nombre del equipo:")
    if not nombre: return
    pais = simpledialog.askstring("Registrar Equipo", "País del equipo:")
    if not pais: return
    
    try:
        equipo = Equipo.crear(nombre.strip(), pais.strip())
        messagebox.showinfo("Éxito", f"Equipo registrado: {equipo.nombre} (ID: {equipo.id_equipo})")
        listar_equipos()
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar equipo:\n{e}")

def modificar_equipo():
    nombre = simpledialog.askstring("Modificar Equipo", "Nombre del equipo a modificar:")
    if not nombre: return
    
    equipo = Equipo.buscar_por_nombre(nombre.strip())
    if not equipo:
        messagebox.showwarning("No encontrado", "Equipo no encontrado.")
        return
    
    nuevo_nombre = simpledialog.askstring("Modificar Equipo", "Nuevo nombre:", initialvalue=equipo.nombre)
    nuevo_pais = simpledialog.askstring("Modificar Equipo", "Nuevo país:", initialvalue=equipo.pais)
    
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE Equipos SET nombre=%s, pais=%s WHERE id_equipo=%s",
                    (nuevo_nombre.strip(), nuevo_pais.strip(), equipo.id_equipo))
        conn.commit()
        messagebox.showinfo("Éxito", "Equipo modificado correctamente.")
        listar_equipos()
    except Exception as e:
        messagebox.showerror("Error", f"Error al modificar equipo:\n{e}")
        if conn: conn.rollback()
    finally:
        if conn: 
            cur.close()
            conn.close()

def eliminar_equipo():
    nombre = simpledialog.askstring("Eliminar Equipo", "Nombre del equipo a eliminar:")
    if not nombre: return
    
    equipo = Equipo.buscar_por_nombre(nombre.strip())
    if not equipo:
        messagebox.showwarning("No encontrado", "Equipo no encontrado.")
        return
    
    if messagebox.askyesno("Confirmar", f"¿Eliminar el equipo '{equipo.nombre}'?"):
        conn = None
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("DELETE FROM Equipos WHERE id_equipo = %s", (equipo.id_equipo,))
            conn.commit()
            messagebox.showinfo("Éxito", "Equipo eliminado.")
            listar_equipos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar equipo:\n{e}")
            if conn: conn.rollback()
        finally:
            if conn:
                cur.close()
                conn.close()

def listar_equipos():
    try:
        equipos = Equipo.listar_todos()
        lb_output.delete(0, tk.END)
        
        if not equipos:
            lb_output.insert(tk.END, "No hay equipos registrados.")
            return
        
        lb_output.insert(tk.END, "=== EQUIPOS ===")
        for eq in equipos:
            lb_output.insert(tk.END, eq.mostrar_equipo())
    except Exception as e:
        messagebox.showerror("Error", f"Error al listar equipos:\n{e}")

# FUNCIONES PARA PILOTOS (CRUD)
def registrar_piloto():
    nombre = simpledialog.askstring("Registrar Piloto", "Nombre del piloto:")
    if not nombre: return
    nacionalidad = simpledialog.askstring("Registrar Piloto", "Nacionalidad:")
    if not nacionalidad: return
    experiencia = simpledialog.askinteger("Registrar Piloto", "Años de experiencia:", minvalue=0, initialvalue=1)
    if experiencia is None: return
    
    puntos = simpledialog.askfloat("Registrar Piloto", "Puntos del piloto:", minvalue=0, initialvalue=0.0)
    if puntos is None: puntos = 0.0
    
    nombre_equipo = simpledialog.askstring("Registrar Piloto", "Nombre del equipo (dejar vacío si no tiene):")
    id_equipo = None
    if nombre_equipo:
        equipo = Equipo.buscar_por_nombre(nombre_equipo.strip())
        if equipo:
            id_equipo = equipo.id_equipo
        else:
            messagebox.showwarning("Equipo no encontrado", "El equipo no existe. Se registrará sin equipo.")
    
    try:
        piloto = Piloto.crear(nombre.strip(), nacionalidad.strip(), experiencia, puntos, id_equipo)
        messagebox.showinfo("Éxito", f"Piloto registrado: {piloto.nombre} (ID: {piloto.id_piloto})")
        listar_pilotos()
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar piloto:\n{e}")

def modificar_piloto():
    nombre = simpledialog.askstring("Modificar Piloto", "Nombre del piloto a modificar:")
    if not nombre: return
    
    piloto = Piloto.buscar_por_nombre(nombre.strip())
    if not piloto:
        messagebox.showwarning("No encontrado", "Piloto no encontrado.")
        return
    
    nuevo_nombre = simpledialog.askstring("Modificar Piloto", "Nuevo nombre:", initialvalue=piloto.nombre)
    nueva_nacionalidad = simpledialog.askstring("Modificar Piloto", "Nueva nacionalidad:", initialvalue=piloto.nacionalidad)
    nueva_experiencia = simpledialog.askinteger("Modificar Piloto", "Nueva experiencia:", initialvalue=piloto.experiencia)
    
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE Pilotos SET nombre=%s, nacionalidad=%s, experiencia=%s WHERE id_piloto=%s",
                    (nuevo_nombre.strip(), nueva_nacionalidad.strip(), nueva_experiencia, piloto.id_piloto))
        conn.commit()
        messagebox.showinfo("Éxito", "Piloto modificado correctamente.")
        listar_pilotos()
    except Exception as e:
        messagebox.showerror("Error", f"Error al modificar piloto:\n{e}")
        if conn: conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()

def eliminar_piloto():
    nombre = simpledialog.askstring("Eliminar Piloto", "Nombre del piloto a eliminar:")
    if not nombre: return
    
    piloto = Piloto.buscar_por_nombre(nombre.strip())
    if not piloto:
        messagebox.showwarning("No encontrado", "Piloto no encontrado.")
        return
    
    if messagebox.askyesno("Confirmar", f"¿Eliminar al piloto '{piloto.nombre}'?"):
        conn = None
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("DELETE FROM Pilotos WHERE id_piloto = %s", (piloto.id_piloto,))
            conn.commit()
            messagebox.showinfo("Éxito", "Piloto eliminado.")
            listar_pilotos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar piloto:\n{e}")
            if conn: conn.rollback()
        finally:
            if conn:
                cur.close()
                conn.close()

def listar_pilotos():
    try:
        pilotos = Piloto.listar_todos()
        lb_output.delete(0, tk.END)
        
        if not pilotos:
            lb_output.insert(tk.END, "No hay pilotos registrados.")
            return
        
        lb_output.insert(tk.END, "=== PILOTOS ===")
        for p in pilotos:
            lb_output.insert(tk.END, p.mostrar_estadisticas())
    except Exception as e:
        messagebox.showerror("Error", f"Error al listar pilotos:\n{e}")

def asignar_puntos_piloto():
    nombre = simpledialog.askstring("Asignar Puntos", "Nombre del piloto:")
    if not nombre: return
    
    piloto = Piloto.buscar_por_nombre(nombre.strip())
    if not piloto:
        messagebox.showwarning("No encontrado", "Piloto no encontrado.")
        return
    
    puntos_nuevos = simpledialog.askfloat("Asignar Puntos", 
        f"Puntos actuales: {piloto.puntos}\n\nPuntos a sumar:", 
        minvalue=0, initialvalue=0)
    
    if puntos_nuevos is None: return
    
    try:
        piloto.puntos += puntos_nuevos
        piloto.actualizar_puntos() # Asumo que esta clase maneja su propia actualización en DB
        messagebox.showinfo("Éxito", f"{piloto.nombre} ahora tiene {piloto.puntos} puntos")
        listar_pilotos()
    except Exception as e:
        messagebox.showerror("Error", f"Error al asignar puntos:\n{e}")


# FUNCIONES PARA AUTOS F1 (CRUD)
def registrar_auto():
    marca = simpledialog.askstring("Registrar Auto", "Marca del auto:")
    if not marca: return
    modelo = simpledialog.askstring("Registrar Auto", "Modelo del auto:")
    if not modelo: return
    velocidad_maxima = simpledialog.askfloat("Registrar Auto", "Velocidad máxima (km/h):", minvalue=0)
    if velocidad_maxima is None: return
    nivel_aerodinamica = simpledialog.askfloat("Registrar Auto", "Nivel aerodinámico (0-10):", minvalue=0, maxvalue=10)
    if nivel_aerodinamica is None: return
    
    nombre_equipo = simpledialog.askstring("Registrar Auto", "Nombre del equipo:")
    if not nombre_equipo: return
    
    equipo = Equipo.buscar_por_nombre(nombre_equipo.strip())
    if not equipo:
        messagebox.showwarning("Equipo no encontrado", "El equipo no existe.")
        return
    
    try:
        auto = AutoDeFormula1.crear(marca.strip(), modelo.strip(), velocidad_maxima, 100.0, 
                                     nivel_aerodinamica, False, equipo.id_equipo)
        messagebox.showinfo("Éxito", f"Auto registrado: {auto.marca} {auto.modelo} (ID: {auto.id_auto})")
        listar_autos()
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar auto:\n{e}")

def modificar_auto():
    id_auto = simpledialog.askinteger("Modificar Auto", "ID del auto a modificar:")
    if not id_auto: return
    
    auto = AutoDeFormula1.buscar_por_id(id_auto)
    if not auto:
        messagebox.showwarning("No encontrado", "Auto no encontrado.")
        return
    
    nueva_marca = simpledialog.askstring("Modificar Auto", "Nueva marca:", initialvalue=auto.marca)
    nuevo_modelo = simpledialog.askstring("Modificar Auto", "Nuevo modelo:", initialvalue=auto.modelo)
    nueva_velocidad = simpledialog.askfloat("Modificar Auto", "Nueva velocidad máxima:", initialvalue=auto.velocidad_maxima)
    
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE AutosF1 SET marca=%s, modelo=%s, velocidadMaxima=%s WHERE id_auto=%s",
                    (nueva_marca.strip(), nuevo_modelo.strip(), nueva_velocidad, auto.id_auto))
        conn.commit()
        messagebox.showinfo("Éxito", "Auto modificado correctamente.")
        listar_autos()
    except Exception as e:
        messagebox.showerror("Error", f"Error al modificar auto:\n{e}")
        if conn: conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()

def eliminar_auto():
    id_auto = simpledialog.askinteger("Eliminar Auto", "ID del auto a eliminar:")
    if not id_auto: return
    
    auto = AutoDeFormula1.buscar_por_id(id_auto)
    if not auto:
        messagebox.showwarning("No encontrado", "Auto no encontrado.")
        return
    
    if messagebox.askyesno("Confirmar", f"¿Eliminar el auto '{auto.marca} {auto.modelo}'?"):
        conn = None
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("DELETE FROM AutosF1 WHERE id_auto = %s", (auto.id_auto,))
            conn.commit()
            messagebox.showinfo("Éxito", "Auto eliminado.")
            listar_autos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar auto:\n{e}")
            if conn: conn.rollback()
        finally:
            if conn:
                cur.close()
                conn.close()

def listar_autos():
    try:
        autos = AutoDeFormula1.listar_todos()
        lb_output.delete(0, tk.END)
        
        if not autos:
            lb_output.insert(tk.END, "No hay autos registrados.")
            return
        
        lb_output.insert(tk.END, "=== AUTOS F1 ===")
        for a in autos:
            lb_output.insert(tk.END, a.mostrar_info())
    except Exception as e:
        messagebox.showerror("Error", f"Error al listar autos:\n{e}")

# FUNCIONES PARA CARRERAS
def registrar_carrera():
    nombre = simpledialog.askstring("Registrar Carrera", "Nombre de la carrera:")
    if not nombre: return
    fecha_str = simpledialog.askstring("Registrar Carrera", "Fecha (YYYY-MM-DD):")
    if not fecha_str: return
    vueltas = simpledialog.askinteger("Registrar Carrera", "Número de vueltas:", minvalue=1)
    if not vueltas: return
    clima = simpledialog.askstring("Registrar Carrera", "Clima:", initialvalue="Soleado")
    
    nombre_circuito = simpledialog.askstring("Registrar Carrera", "Nombre del circuito:")
    if not nombre_circuito: return
    
    circuito = Circuito.buscar_por_nombre(nombre_circuito.strip())
    if not circuito:
        messagebox.showwarning("Circuito no encontrado", "El circuito no existe.")
        return
    
    try:
        carrera = Carrera.crear(nombre.strip(), fecha_str, vueltas, clima.strip(), circuito.id_circuito)
        messagebox.showinfo("Éxito", f"Carrera registrada: {carrera.nombre} (ID: {carrera.id_carrera})")
        listar_carreras()
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar carrera:\n{e}")

def listar_carreras():
    try:
        carreras = Carrera.listar_todas()
        lb_output.delete(0, tk.END)
        
        if not carreras:
            lb_output.insert(tk.END, "No hay carreras registradas.")
            return
        
        lb_output.insert(tk.END, "=== CARRERAS ===")
        for c in carreras:
            lb_output.insert(tk.END, f"[{c.id_carrera}] {c.nombre} - {c.fecha} ({c.vueltas} vueltas)")
    except Exception as e:
        messagebox.showerror("Error", f"Error al listar carreras:\n{e}")
        
def registrar_resultado_carrera():
    nombre_carrera = simpledialog.askstring("Registrar Resultado", "Nombre de la carrera:")
    if not nombre_carrera: return
    carrera = Carrera.buscar_por_nombre(nombre_carrera.strip())
    if not carrera:
        messagebox.showwarning("No encontrada", "Carrera no encontrada.")
        return
    
    nombre_piloto = simpledialog.askstring("Registrar Resultado", "Nombre del piloto:")
    if not nombre_piloto: return
    piloto = Piloto.buscar_por_nombre(nombre_piloto.strip())
    if not piloto:
        messagebox.showwarning("No encontrado", "Piloto no encontrado.")
        return
    
    posicion = simpledialog.askinteger("Registrar Resultado", "Posición final (1-20):", minvalue=1, maxvalue=20)
    if not posicion: return
    
    tiempo_str = simpledialog.askstring("Registrar Resultado", "Tiempo total (HH:MM:SS):", initialvalue="01:30:45")
    if not tiempo_str: return
    
    puntos_f1 = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}
    puntos_obtenidos = puntos_f1.get(posicion, 0)
    
    try:
        carrera.registrar_resultado(piloto.id_piloto, posicion, tiempo_str, puntos_obtenidos)
        
        # Asumo que el objeto Piloto tiene un método para actualizar puntos
        piloto.puntos += puntos_obtenidos
        piloto.actualizar_puntos()
        
        messagebox.showinfo("Éxito", f"Resultado registrado:\nPiloto: {piloto.nombre}\nPosición: {posicion}°\nPuntos obtenidos: {puntos_obtenidos}\nTotal acumulado: {piloto.puntos}")
        
        listar_pilotos()
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar resultado:\n{e}")

def ver_resultados_carrera():
    nombre = simpledialog.askstring("Ver Resultados", "Nombre de la carrera:")
    if not nombre: return
    
    carrera = Carrera.buscar_por_nombre(nombre.strip())
    if not carrera:
        messagebox.showwarning("No encontrada", "Carrera no encontrada.")
        return
    
    try:
        resultados = carrera.mostrar_resultados()
        lb_output.delete(0, tk.END)
        
        if not resultados:
            lb_output.insert(tk.END, f"No hay resultados para la carrera '{carrera.nombre}'.")
            return
        
        lb_output.insert(tk.END, f"=== RESULTADOS: {carrera.nombre} ===")
        for r in resultados:
            lb_output.insert(tk.END, f"{r[0]}° - {r[1]} | Tiempo: {r[2]} | Puntos: {r[3]}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al mostrar resultados:\n{e}")
        
# FUNCIONES PARA CIRCUITOS (CRUD)

def registrar_circuito():
    nombre = simpledialog.askstring("Registrar Circuito", "Nombre del circuito:")
    if not nombre: return
    pais = simpledialog.askstring("Registrar Circuito", "País:")
    if not pais: return
    longitud = simpledialog.askfloat("Registrar Circuito", "Longitud (km):", minvalue=0)
    if longitud is None: return
    curvas = simpledialog.askinteger("Registrar Circuito", "Número de curvas:", minvalue=0)
    if curvas is None: return
    
    try:
        circuito = Circuito.crear(nombre.strip(), pais.strip(), longitud, curvas)
        messagebox.showinfo("Éxito", f"Circuito registrado: {circuito.nombre} (ID: {circuito.id_circuito})")
        listar_circuitos()
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar circuito:\n{e}")

def listar_circuitos():
    try:
        circuitos = Circuito.listar_todos()
        lb_output.delete(0, tk.END)
        
        if not circuitos:
            lb_output.insert(tk.END, "No hay circuitos registrados.")
            return
        
        lb_output.insert(tk.END, "=== CIRCUITOS ===")
        for c in circuitos:
            lb_output.insert(tk.END, c.mostrar_datos_circuito())
    except Exception as e:
        messagebox.showerror("Error", f"Error al listar circuitos:\n{e}")

# FUNCIÓN PARA SALIR
def salir():
    """Cierra la aplicación"""
    if MAIN_WINDOW:
        MAIN_WINDOW.destroy()
    sys.exit(0)

# ====================================================================
# CONFIGURACIÓN DE INTERFAZ PRINCIPAL CON RESTRICCIÓN DE ROLES
# ====================================================================

def inicializar_interfaz_principal(root, rol):
    """Configura la ventana principal después del login, ajustando permisos."""
    global lb_output # Hacemos la ListBox global para que las funciones CRUD la usen
    
    # ----------------------------------------------------
    # 1. Menú principal (tk.Menu)
    # ----------------------------------------------------
    menubar = tk.Menu(root)

    # Menú EQUIPOS
    menu_equipos = tk.Menu(menubar, tearoff=0)
    if rol == 'admin':
        menu_equipos.add_command(label="Registrar equipo", command=registrar_equipo)
        menu_equipos.add_command(label="Modificar equipo", command=modificar_equipo)
        menu_equipos.add_command(label="Eliminar equipo", command=eliminar_equipo)
        menu_equipos.add_separator()
    menu_equipos.add_command(label="Listar equipos", command=listar_equipos)
    menubar.add_cascade(label="Equipos", menu=menu_equipos)

    # Menú PILOTOS
    menu_pilotos = tk.Menu(menubar, tearoff=0)
    if rol == 'admin':
        menu_pilotos.add_command(label="Registrar piloto", command=registrar_piloto)
        menu_pilotos.add_command(label="Modificar piloto", command=modificar_piloto)
        menu_pilotos.add_command(label="Eliminar piloto", command=eliminar_piloto)
        menu_pilotos.add_command(label="Asignar puntos", command=asignar_puntos_piloto)
        menu_pilotos.add_separator()
    menu_pilotos.add_command(label="Listar pilotos", command=listar_pilotos)
    menubar.add_cascade(label="Pilotos", menu=menu_pilotos)

    # Menú AUTOS
    menu_autos = tk.Menu(menubar, tearoff=0)
    if rol == 'admin':
        menu_autos.add_command(label="Registrar auto", command=registrar_auto)
        menu_autos.add_command(label="Modificar auto", command=modificar_auto)
        menu_autos.add_command(label="Eliminar auto", command=eliminar_auto)
        menu_autos.add_separator()
    menu_autos.add_command(label="Listar autos", command=listar_autos)
    menubar.add_cascade(label="Autos", menu=menu_autos)

    # Menú CARRERAS
    menu_carreras = tk.Menu(menubar, tearoff=0)
    if rol == 'admin':
        menu_carreras.add_command(label="Registrar carrera", command=registrar_carrera)
        menu_carreras.add_command(label="Registrar resultado", command=registrar_resultado_carrera)
        menu_carreras.add_separator()
    menu_carreras.add_command(label="Listar carreras", command=listar_carreras)
    menu_carreras.add_command(label="Ver resultados", command=ver_resultados_carrera)
    menubar.add_cascade(label="Carreras", menu=menu_carreras)

    # Menú CIRCUITOS
    menu_circuitos = tk.Menu(menubar, tearoff=0)
    if rol == 'admin':
        menu_circuitos.add_command(label="Registrar circuito", command=registrar_circuito)
        menu_circuitos.add_separator()
    menu_circuitos.add_command(label="Listar circuitos", command=listar_circuitos)
    menubar.add_cascade(label="Circuitos", menu=menu_circuitos)

    # Menú ARCHIVO
    menu_archivo = tk.Menu(menubar, tearoff=0)
    menu_archivo.add_command(label="Salir", command=salir)
    menubar.add_cascade(label="Archivo", menu=menu_archivo)

    root.config(menu=menubar)
    
    # ----------------------------------------------------
    # 2. Frame y Listbox de Salida
    # ----------------------------------------------------
    frame_output = ttk.Frame(root, padding=(12, 12))
    frame_output.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

    lbl_output = ttk.Label(frame_output, text=f"Sistema de Gestión F1 (Rol: {rol.capitalize()})", font=("Segoe UI", 14, "bold"))
    lbl_output.pack(anchor="w")

    frame_list = ttk.Frame(frame_output)
    frame_list.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

    sb = ttk.Scrollbar(frame_list, orient=tk.VERTICAL)
    lb_output = tk.Listbox(frame_list, yscrollcommand=sb.set, font=("Consolas", 10))
    sb.config(command=lb_output.yview)
    sb.pack(side=tk.RIGHT, fill=tk.Y)
    lb_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Mensaje de ayuda
    lbl_help = ttk.Label(frame_output, text="Usa el menú superior para gestionar el sistema", font=("Segoe UI", 9))
    lbl_help.pack(anchor="w", pady=(8, 0))
    
    # 3. Mostrar equipos al iniciar
    root.after(100, listar_equipos)

    root.mainloop()

# ====================================================================
# PUNTO DE ENTRADA DE LA APLICACIÓN
# ====================================================================

if __name__ == "__main__":
    mostrar_ventana_login()