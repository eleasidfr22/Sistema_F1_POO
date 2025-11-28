# execute.py
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

from src.equipo import Equipo
from src.piloto import Piloto
from src.auto_formula1 import AutoDeFormula1
from src.carrera import Carrera
from src.circuito import Circuito
from src.mecanico import Mecanico

# FUNCIONES PARA EQUIPOS (CRUD)

def registrar_equipo():
    """Registra un nuevo equipo"""
    nombre = simpledialog.askstring("Registrar Equipo", "Nombre del equipo:")
    if not nombre:
        return
    pais = simpledialog.askstring("Registrar Equipo", "País del equipo:")
    if not pais:
        return
    
    try:
        equipo = Equipo.crear(nombre.strip(), pais.strip())
        messagebox.showinfo("Éxito", f"Equipo registrado: {equipo.nombre} (ID: {equipo.id_equipo})")
        listar_equipos()
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar equipo:\n{e}")

def modificar_equipo():
    """Modifica un equipo existente"""
    nombre = simpledialog.askstring("Modificar Equipo", "Nombre del equipo a modificar:")
    if not nombre:
        return
    
    equipo = Equipo.buscar_por_nombre(nombre.strip())
    if not equipo:
        messagebox.showwarning("No encontrado", "Equipo no encontrado.")
        return
    
    nuevo_nombre = simpledialog.askstring("Modificar Equipo", "Nuevo nombre:", initialvalue=equipo.nombre)
    nuevo_pais = simpledialog.askstring("Modificar Equipo", "Nuevo país:", initialvalue=equipo.pais)
    
    try:
        from conexion_db import get_conn
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE Equipos SET nombre=%s, pais=%s WHERE id_equipo=%s",
                   (nuevo_nombre.strip(), nuevo_pais.strip(), equipo.id_equipo))
        conn.commit()
        cur.close()
        conn.close()
        messagebox.showinfo("Éxito", "Equipo modificado correctamente.")
        listar_equipos()
    except Exception as e:
        messagebox.showerror("Error", f"Error al modificar equipo:\n{e}")

def eliminar_equipo():
    """Elimina un equipo"""
    nombre = simpledialog.askstring("Eliminar Equipo", "Nombre del equipo a eliminar:")
    if not nombre:
        return
    
    equipo = Equipo.buscar_por_nombre(nombre.strip())
    if not equipo:
        messagebox.showwarning("No encontrado", "Equipo no encontrado.")
        return
    
    if messagebox.askyesno("Confirmar", f"¿Eliminar el equipo '{equipo.nombre}'?"):
        try:
            from conexion_db import get_conn
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("DELETE FROM Equipos WHERE id_equipo = %s", (equipo.id_equipo,))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Éxito", "Equipo eliminado.")
            listar_equipos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar equipo:\n{e}")

def listar_equipos():
    """Lista todos los equipos"""
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
    """Registra un nuevo piloto"""
    nombre = simpledialog.askstring("Registrar Piloto", "Nombre del piloto:")
    if not nombre:
        return
    nacionalidad = simpledialog.askstring("Registrar Piloto", "Nacionalidad:")
    if not nacionalidad:
        return
    experiencia = simpledialog.askinteger("Registrar Piloto", "Años de experiencia:", minvalue=0, initialvalue=1)
    if experiencia is None:
        return
    
    # Opcion para asignar piloto a un equipo
    nombre_equipo = simpledialog.askstring("Registrar Piloto", "Nombre del equipo (dejar vacío si no tiene):")
    id_equipo = None
    if nombre_equipo:
        equipo = Equipo.buscar_por_nombre(nombre_equipo.strip())
        if equipo:
            id_equipo = equipo.id_equipo
        else:
            messagebox.showwarning("Equipo no encontrado", "El equipo no existe. Se registrará sin equipo.")
    
    try:
        piloto = Piloto.crear(nombre.strip(), nacionalidad.strip(), experiencia, 0.0, id_equipo)
        messagebox.showinfo("Éxito", f"Piloto registrado: {piloto.nombre} (ID: {piloto.id_piloto})")
        listar_pilotos()
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar piloto:\n{e}")

def modificar_piloto():
    """Modifica un piloto existente"""
    nombre = simpledialog.askstring("Modificar Piloto", "Nombre del piloto a modificar:")
    if not nombre:
        return
    
    piloto = Piloto.buscar_por_nombre(nombre.strip())
    if not piloto:
        messagebox.showwarning("No encontrado", "Piloto no encontrado.")
        return
    
    nuevo_nombre = simpledialog.askstring("Modificar Piloto", "Nuevo nombre:", initialvalue=piloto.nombre)
    nueva_nacionalidad = simpledialog.askstring("Modificar Piloto", "Nueva nacionalidad:", initialvalue=piloto.nacionalidad)
    nueva_experiencia = simpledialog.askinteger("Modificar Piloto", "Nueva experiencia:", initialvalue=piloto.experiencia)
    
    try:
        from conexion_db import get_conn
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE Pilotos SET nombre=%s, nacionalidad=%s, experiencia=%s WHERE id_piloto=%s",
                   (nuevo_nombre.strip(), nueva_nacionalidad.strip(), nueva_experiencia, piloto.id_piloto))
        conn.commit()
        cur.close()
        conn.close()
        messagebox.showinfo("Éxito", "Piloto modificado correctamente.")
        listar_pilotos()
    except Exception as e:
        messagebox.showerror("Error", f"Error al modificar piloto:\n{e}")

def eliminar_piloto():
    """Elimina un piloto"""
    nombre = simpledialog.askstring("Eliminar Piloto", "Nombre del piloto a eliminar:")
    if not nombre:
        return
    
    piloto = Piloto.buscar_por_nombre(nombre.strip())
    if not piloto:
        messagebox.showwarning("No encontrado", "Piloto no encontrado.")
        return
    
    if messagebox.askyesno("Confirmar", f"¿Eliminar al piloto '{piloto.nombre}'?"):
        try:
            from conexion_db import get_conn
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("DELETE FROM Pilotos WHERE id_piloto = %s", (piloto.id_piloto,))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Éxito", "Piloto eliminado.")
            listar_pilotos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar piloto:\n{e}")

def listar_pilotos():
    """Lista todos los pilotos"""
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

# FUNCIONES PARA AUTOS F1 (CRUD)

def registrar_auto():
    """Registra un nuevo auto F1"""
    marca = simpledialog.askstring("Registrar Auto", "Marca del auto:")
    if not marca:
        return
    modelo = simpledialog.askstring("Registrar Auto", "Modelo del auto:")
    if not modelo:
        return
    velocidad_maxima = simpledialog.askfloat("Registrar Auto", "Velocidad máxima (km/h):", minvalue=0)
    if velocidad_maxima is None:
        return
    nivel_aerodinamica = simpledialog.askfloat("Registrar Auto", "Nivel aerodinámico (0-10):", minvalue=0, maxvalue=10)
    if nivel_aerodinamica is None:
        return
    
    # Asignar a un equipo
    nombre_equipo = simpledialog.askstring("Registrar Auto", "Nombre del equipo:")
    if not nombre_equipo:
        return
    
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
    """Modifica un auto existente"""
    id_auto = simpledialog.askinteger("Modificar Auto", "ID del auto a modificar:")
    if not id_auto:
        return
    
    auto = AutoDeFormula1.buscar_por_id(id_auto)
    if not auto:
        messagebox.showwarning("No encontrado", "Auto no encontrado.")
        return
    
    nueva_marca = simpledialog.askstring("Modificar Auto", "Nueva marca:", initialvalue=auto.marca)
    nuevo_modelo = simpledialog.askstring("Modificar Auto", "Nuevo modelo:", initialvalue=auto.modelo)
    nueva_velocidad = simpledialog.askfloat("Modificar Auto", "Nueva velocidad máxima:", initialvalue=auto.velocidad_maxima)
    
    try:
        from conexion_db import get_conn
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE AutosF1 SET marca=%s, modelo=%s, velocidadMaxima=%s WHERE id_auto=%s",
                   (nueva_marca.strip(), nuevo_modelo.strip(), nueva_velocidad, auto.id_auto))
        conn.commit()
        cur.close()
        conn.close()
        messagebox.showinfo("Éxito", "Auto modificado correctamente.")
        listar_autos()
    except Exception as e:
        messagebox.showerror("Error", f"Error al modificar auto:\n{e}")

def eliminar_auto():
    """Elimina un auto"""
    id_auto = simpledialog.askinteger("Eliminar Auto", "ID del auto a eliminar:")
    if not id_auto:
        return
    
    auto = AutoDeFormula1.buscar_por_id(id_auto)
    if not auto:
        messagebox.showwarning("No encontrado", "Auto no encontrado.")
        return
    
    if messagebox.askyesno("Confirmar", f"¿Eliminar el auto '{auto.marca} {auto.modelo}'?"):
        try:
            from conexion_db import get_conn
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("DELETE FROM AutosF1 WHERE id_auto = %s", (auto.id_auto,))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Éxito", "Auto eliminado.")
            listar_autos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar auto:\n{e}")

def listar_autos():
    """Lista todos los autos F1"""
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

# FUNCIONES PARA CARRERAS (CRUD)

def registrar_carrera():
    """Registra una nueva carrera"""
    nombre = simpledialog.askstring("Registrar Carrera", "Nombre de la carrera:")
    if not nombre:
        return
    fecha_str = simpledialog.askstring("Registrar Carrera", "Fecha (YYYY-MM-DD):")
    if not fecha_str:
        return
    vueltas = simpledialog.askinteger("Registrar Carrera", "Número de vueltas:", minvalue=1)
    if not vueltas:
        return
    clima = simpledialog.askstring("Registrar Carrera", "Clima:", initialvalue="Soleado")
    
    # Asignar circuito
    nombre_circuito = simpledialog.askstring("Registrar Carrera", "Nombre del circuito:")
    if not nombre_circuito:
        return
    
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
    """Lista todas las carreras"""
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

def ver_resultados_carrera():
    """Muestra los resultados de una carrera"""
    nombre = simpledialog.askstring("Ver Resultados", "Nombre de la carrera:")
    if not nombre:
        return
    
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
    """Registra un nuevo circuito"""
    nombre = simpledialog.askstring("Registrar Circuito", "Nombre del circuito:")
    if not nombre:
        return
    pais = simpledialog.askstring("Registrar Circuito", "País:")
    if not pais:
        return
    longitud = simpledialog.askfloat("Registrar Circuito", "Longitud (km):", minvalue=0)
    if longitud is None:
        return
    curvas = simpledialog.askinteger("Registrar Circuito", "Número de curvas:", minvalue=0)
    if curvas is None:
        return
    
    try:
        circuito = Circuito.crear(nombre.strip(), pais.strip(), longitud, curvas)
        messagebox.showinfo("Éxito", f"Circuito registrado: {circuito.nombre} (ID: {circuito.id_circuito})")
        listar_circuitos()
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar circuito:\n{e}")

def listar_circuitos():
    """Lista todos los circuitos"""
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
    root.destroy()
    sys.exit(0)

# VENTANA PRINCIPAL

root = tk.Tk()
root.title("Sistema de Gestión F1 - Interfaz Gráfica")
root.geometry("900x600")
root.minsize(800, 500)

# Menú principal
menubar = tk.Menu(root)

# Menú EQUIPOS
menu_equipos = tk.Menu(menubar, tearoff=0)
menu_equipos.add_command(label="Registrar equipo", command=registrar_equipo)
menu_equipos.add_command(label="Modificar equipo", command=modificar_equipo)
menu_equipos.add_command(label="Eliminar equipo", command=eliminar_equipo)
menu_equipos.add_separator()
menu_equipos.add_command(label="Listar equipos", command=listar_equipos)
menubar.add_cascade(label="Equipos", menu=menu_equipos)

# Menú PILOTOS
menu_pilotos = tk.Menu(menubar, tearoff=0)
menu_pilotos.add_command(label="Registrar piloto", command=registrar_piloto)
menu_pilotos.add_command(label="Modificar piloto", command=modificar_piloto)
menu_pilotos.add_command(label="Eliminar piloto", command=eliminar_piloto)
menu_pilotos.add_separator()
menu_pilotos.add_command(label="Listar pilotos", command=listar_pilotos)
menubar.add_cascade(label="Pilotos", menu=menu_pilotos)

# Menú AUTOS
menu_autos = tk.Menu(menubar, tearoff=0)
menu_autos.add_command(label="Registrar auto", command=registrar_auto)
menu_autos.add_command(label="Modificar auto", command=modificar_auto)
menu_autos.add_command(label="Eliminar auto", command=eliminar_auto)
menu_autos.add_separator()
menu_autos.add_command(label="Listar autos", command=listar_autos)
menubar.add_cascade(label="Autos", menu=menu_autos)

# Menú CARRERAS
menu_carreras = tk.Menu(menubar, tearoff=0)
menu_carreras.add_command(label="Registrar carrera", command=registrar_carrera)
menu_carreras.add_command(label="Listar carreras", command=listar_carreras)
menu_carreras.add_command(label="Ver resultados", command=ver_resultados_carrera)
menubar.add_cascade(label="Carreras", menu=menu_carreras)

# Menú CIRCUITOS
menu_circuitos = tk.Menu(menubar, tearoff=0)
menu_circuitos.add_command(label="Registrar circuito", command=registrar_circuito)
menu_circuitos.add_command(label="Listar circuitos", command=listar_circuitos)
menubar.add_cascade(label="Circuitos", menu=menu_circuitos)

# Menú ARCHIVO
menu_archivo = tk.Menu(menubar, tearoff=0)
menu_archivo.add_command(label="Salir", command=salir)
menubar.add_cascade(label="Archivo", menu=menu_archivo)

root.config(menu=menubar)

frame_output = ttk.Frame(root, padding=(12, 12))
frame_output.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

lbl_output = ttk.Label(frame_output, text="Sistema de Gestión F1", font=("Segoe UI", 14, "bold"))
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

# Mostrar equipos al iniciar
root.after(100, listar_equipos)

root.mainloop()