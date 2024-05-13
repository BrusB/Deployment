import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation  # Importa FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk
from tkinter import ttk
import pkg_resources
from ttkthemes import ThemedTk
from tkinter import Toplevel, Text, Scrollbar
import subprocess
import os
import sys

global ventana
# Función para obtener información sobre los discos
def obtener_info_discos():
    discos = psutil.disk_partitions()
    info_discos = ""
    for disco in discos:
        # Verificar si el dispositivo es un dispositivo "loop"
        if "loop" not in disco.device:
            info_discos += f"Disco: {disco.device}\n"
            info_discos += f"  Punto de montaje: {disco.mountpoint}\n"
            info_discos += f"  Tipo: {disco.fstype}\n"

        # Obtener información sobre el uso del disco
            uso_disco = psutil.disk_usage(disco.mountpoint)
            info_discos += f"  Tamaño total: {bytes_to_gb(uso_disco.total)} GB\n"
            info_discos += f"  Espacio utilizado: {bytes_to_gb(uso_disco.used)} GB\n"
            info_discos += f"  Espacio libre: {bytes_to_gb(uso_disco.free)} GB\n\n"
    return info_discos
    

# Función para obtener información sobre las aplicaciones instaladas (subprocess)

def obtener_info_aplicaciones():
    aplicaciones = ""
    try:
        # Ejecutar el comando dpkg para obtener la lista de paquetes instalados
        resultado = subprocess.run(['dpkg', '--get-selections'], capture_output=True, text=True)
        if resultado.returncode == 0:
            # Obtener la salida del comando y dividirla en líneas
            lineas = resultado.stdout.split('\n')
            for linea in lineas:
                # Cada línea tiene el formato "nombre_del_paquete estado"
                # Dividimos la línea para obtener el nombre del paquete
                partes = linea.split('\t')
                if len(partes) > 1:
                    aplicaciones += f"- {partes[0]}\n"
        else:
            aplicaciones = "Error al obtener la lista de aplicaciones instaladas."
            print(f"Error: {resultado.stderr}")
    except Exception as e:
        aplicaciones = "Error al obtener la lista de aplicaciones instaladas."
        print(f"Error: {e}")
    return aplicaciones
    
# Función para obtener información sobre la actividad de red
def obtener_info_red():
    redes = psutil.net_io_counters(pernic=True)
    info_red = ""
    for interfaz, red in redes.items():
        info_red += f"Interfaz: {interfaz}\n"
        info_red += f"  Bytes recibidos: {bytes_to_mb(red.bytes_recv)} MB\n"
        info_red += f"  Bytes enviados: {bytes_to_mb(red.bytes_sent)} MB\n"
        info_red += f"  Paquetes recibidos: {red.packets_recv}\n"
        info_red += f"  Paquetes enviados: {red.packets_sent}\n\n"
    return info_red
    
def obtener_info_rendimiento():
        cpu_percent = psutil.cpu_percent()
        mem_percent = psutil.virtual_memory().percent
        return cpu_percent, mem_percent    
# Función para convertir bytes a gigabytes
def bytes_to_gb(bytes):
    return round(bytes / (1024 ** 3), 2)
    
# Función para convertir bytes a megabytes
def bytes_to_mb(bytes):
    return round(bytes / (1024 ** 2), 2)
    
# Función para mostrar la versión
def mostrar_version():
    version_window = tk.Toplevel() # Crea una nueva ventana superior asociada a la ventana principal
    version_window.title("Versión")  # Título de la ventana
    version_window.geometry("200x100")  # Tamaño de la ventana
    # Asegúrate de que la ventana de la versión aparezca por delante de la ventana principal
    version_window.lift()
    version_window.focus_force()  # Obtener el foco de la ventana
    label = tk.Label(version_window, text="Versión 1.11")
    label.pack()

def obtener_procesos_ejecucion():
    try:
        resultado = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        if resultado.returncode == 0:
            return resultado.stdout.splitlines()
        else:
            return ['Error: No se pueden obtener los procesos en ejecución']
    except Exception as e:
        return [f'Error: {str(e)}']
    
# Función para mostrar los procesos en una ventana emergente
# Función para mostrar los procesos en una ventana emergente
def mostrar_procesos():
    # Crear una ventana emergente
    ventana_procesos = Toplevel()
    ventana_procesos.title("Procesos en Ejecución")

    # Crear un cuadro de búsqueda
    lbl_buscar = ttk.Label(ventana_procesos, text="Buscar:")
    lbl_buscar.pack(side="top", padx=10, pady=5)
    entry_buscar = ttk.Entry(ventana_procesos, width=50)
    entry_buscar.pack(side="top", padx=10, pady=5)
    
    # Crear un cuadro para ingresar el PID
    lbl_pid = ttk.Label(ventana_procesos, text="PID:")
    lbl_pid.pack(side="top", padx=10, pady=5)
    entry_pid = ttk.Entry(ventana_procesos, width=50)
    entry_pid.pack(side="top", padx=10, pady=5)

    # Crear un widget de texto para mostrar los procesos
    txt_procesos = Text(ventana_procesos, height=20, width=100)
    txt_procesos.pack(side="left", fill="both", expand=True)

    # Agregar una barra de desplazamiento para el widget de texto
    scrollbar = Scrollbar(ventana_procesos, command=txt_procesos.yview)
    scrollbar.pack(side="right", fill="y")
    txt_procesos.config(yscrollcommand=scrollbar.set)

    # Obtener los procesos en ejecución
    procesos = obtener_procesos_ejecucion()
    
    # Mostrar los procesos en el widget de texto
    for proceso in procesos:
        txt_procesos.insert("end", proceso + "\n")
    

     # Función para buscar procesos
    def buscar_proceso():
        texto_busqueda = entry_buscar.get()
        txt_procesos.tag_remove("found", "1.0", "end")
        if texto_busqueda:
            inicio = "1.0"
            while True:
                inicio = txt_procesos.search(texto_busqueda, inicio, nocase=1, stopindex="end")
                if not inicio:
                    break
                fin = f"{inicio}+{len(texto_busqueda)}c"
                txt_procesos.tag_add("found", inicio, fin)
                inicio = fin
            txt_procesos.tag_config("found", background="yellow")

    # Función para matar un proceso seleccionado
    def matar_proceso():
        pid = entry_pid.get()
        if pid:
            subprocess.run(["kill", pid])

    # Botón para buscar procesos
    btn_buscar = ttk.Button(ventana_procesos, text="Buscar", command=buscar_proceso)
    btn_buscar.pack(side="top", padx=10, pady=5)

    # Botón para matar el proceso seleccionado
    btn_matar = ttk.Button(ventana_procesos, text="Kill", command=matar_proceso)
    btn_matar.pack(side="top", padx=10, pady=5)
# Función para actualizar los datos de los gráficos de CPU y memoria
def update_plots(frame, ax1, ax2):
    cpu_percent, mem_percent = obtener_info_rendimiento()
    ax1.clear()
    ax2.clear()
    ax1.pie([cpu_percent, 100 - cpu_percent], labels=['CPU', ''], autopct='%1.1f%%', startangle=140, colors=['#8195F8', 'lightgray'])
    ax2.pie([mem_percent, 100 - mem_percent], labels=['Memoria', ''], autopct='%1.1f%%', startangle=140, colors=['#FBFB78', 'lightgray'])
    ax1.set_title('Uso de CPU')
    ax2.set_title('Uso de Memoria')


def reiniciar_apache():
    try:
        # Ejecuta el comando para reiniciar Apache con pkexec para la autenticación gráfica
        result = subprocess.run(['sudo', 'service', 'apache2', 'restart'], check=True)
        print("Servicio Apache reiniciado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al reiniciar Apache: {e}")
    except Exception as e:
        # Esto imprime otros errores, como problemas al lanzar pkexec
        print(f"Error general: {e}")

def reiniciar_mysql():
    try:
        # comando para reinciar servicio, usamos pkexec para la autenticación gráfica
        result = subprocess.run(['sudo', 'service', 'mysql', 'restart'], check=True)
        # Si el comando fue exitoso, imprimirá esto:
        print("Servicio MySQL reiniciado correctamente.")
    except subprocess.CalledProcessError as e:
        # Que imprima errores si falla el reincio
        print(f"Error al reiniciar MySQL: {e}")
    except Exception as e:
       # que imprima otro tipo de errores:
        print(f"Error general: {e}")


# Función principal para crear la interfaz de usuario
def crear_interfaz():

    # Configuración de la ventana principal
    ventana = ThemedTk(theme="radiance")  # Puedes cambiar el tema a tu preferencia

    # Ejecutar el comando hostname y capturar la salida
    resultado = subprocess.run(["hostname"], capture_output=True, text=True)
    hostname = resultado.stdout.strip()  # Obtener el nombre del host y eliminar espacios en blannco 

    # nombre titulo y nombre del equipo
    ventana.title(f"@RGOS - {hostname}")

    # fondo
    ventana.configure(background="#E2B8F3")
    
    # Tamaño y posición de la ventana
    ventana.geometry("1920x1080")

 # Configura la grilla para que el canvas se ajuste con el tamaño de la ventana
    ventana.grid_columnconfigure(2, weight=1)
    ventana.grid_rowconfigure(0, weight=1)

    # Función para obtener el porcentaje de uso de CPU y memoria
    def obtener_info_rendimiento():
        cpu_percent = psutil.cpu_percent()
        mem_percent = psutil.virtual_memory().percent
        return cpu_percent, mem_percent 
    
# Función para actualizar el gráfico circular con los nuevos datos de uso de CPU y memoria
    

# Obtener los datos de uso de CPU y memoria
    cpu_percent, mem_percent = obtener_info_rendimiento()

    # Configurar colores
    color_cpu = '#8195F8'  # Color para la sección de CPU
    color_memoria = '#FBFB78'  # Color para la sección de Memoria

    # Crear un Figure que contenga ambos gráficos
    fig = plt.Figure(figsize=(3, 3), dpi=100)
    global ax1, ax2
    ax1 = fig.add_subplot(211)  # Subplot para el gráfico de CPU
    ax2 = fig.add_subplot(212)  # Subplot para el gráfico de memoria

    # Dibujar los gráficos en los subplots
    ax1.pie([cpu_percent, 100 - cpu_percent], labels=['CPU', ''], autopct='%1.1f%%', startangle=140, colors=[color_cpu, 'lightgray'])
    ax2.pie([mem_percent, 100 - mem_percent], labels=['Memoria', ''], autopct='%1.1f%%', startangle=140, colors=[color_memoria, 'lightgray'])

    # Configurar los subplots
    ax1.set_title('Uso de CPU')
    ax2.set_title('Uso de Memoria')

    # Crear un canvas para mostrar el Figure
    global canvas
    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.draw()
    ventana.update()
    # Colocar el canvas en la ventana
    canvas.get_tk_widget().grid(row=1, column=2, padx=10, pady=5, sticky="nsew")

    # Crear la animación para actualizar los gráfcco
    # Crear la animación para actualizar los gráficos
    ani = FuncAnimation(fig, update_plots, fargs=(ax1, ax2), frames=10, interval=4000)  # 10 fotogramas, intervalo de 1000 ms
    print(f"Porcentaje de CPU incial:{cpu_percent}%")
    print(f"Porcentaje de Memoria incial:{mem_percent}%")
    
    def obtener_info_rendimiento():
        cpu_percent = psutil.cpu_percent()
        mem_percent = psutil.virtual_memory().percent
        return cpu_percent, mem_percent


    # Sección de discos
    lbl_discos = ttk.Label(ventana, text="INFORMACIÓN DE DISCOS:")
    lbl_discos.grid(row=0, column=0, sticky="w", padx=10, pady=5)
    txt_discos = tk.Text(ventana, height=20, width=50)
    txt_discos.insert(tk.END, obtener_info_discos())
    txt_discos.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
    
    # Sección de aplicaciones instaladas
    lbl_aplicaciones = ttk.Label(ventana, text="APLICACIONES INSTALADAS:")
    lbl_aplicaciones.grid(row=2, column=0, sticky="w", padx=10, pady=5)

    # Crear el widget de texto
    txt_aplicaciones = tk.Text(ventana, height=20, width=50)
    txt_aplicaciones.insert(tk.END, obtener_info_aplicaciones())
    txt_aplicaciones.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

    # Crear una barra de desplazamiento vertical para el widget Text
    scrollbar = tk.Scrollbar(ventana, command=txt_aplicaciones.yview)
    scrollbar.grid(row=3, column=1, padx=(0,10), pady=5, sticky="ns")

    # Configurar la relación entre la barra de desplazamiento y el widget de texto
    txt_aplicaciones.config(yscrollcommand=scrollbar.set)

    
    # Sección de actividad de red
    lbl_red = ttk.Label(ventana, text="INTERFACES")
    lbl_red.grid(row=0, column=1, sticky="w", padx=10, pady=5)
    txt_red = tk.Text(ventana, height=20, width=50)
    txt_red.insert(tk.END, obtener_info_red())
    txt_red.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

    # Crear un gráfico de barras para visualizar la actividad de red
    fig = plt.Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    interfaces = []
    bytes_recv = []
    bytes_sent = []
    for interfaz, red in psutil.net_io_counters(pernic=True).items():
        interfaces.append(interfaz)
        bytes_recv.append(bytes_to_mb(red.bytes_recv))
        bytes_sent.append(bytes_to_mb(red.bytes_sent))
    x = np.arange(len(interfaces))
    width = 0.35
    # Especificar los colores de las barras
    color_bytes_recv = '#8195F8'  # Color para los bytes recibidos
    color_bytes_sent = '#FBFB78'  # Color para los bytes enviados
    ax.bar(x - width/2, bytes_recv, width, color=color_bytes_recv, label='Bytes Recibidos')
    ax.bar(x + width/2, bytes_sent, width, color=color_bytes_sent, label='Bytes Enviados')
    ax.set_xticks(x)
    ax.set_xticklabels(interfaces)
    ax.legend()
    ax.set_xlabel('Interfaz')
    ax.set_ylabel('MB')
    ax.set_title('Actividad de Red')
    ax.set_ylim(0, 200)  # Establece el rango de 0 a 300 megabytes en el eje vertical  
    ax.set_yticks(np.arange(0, 210, 10))    # Marcar en intervalos de 20 megabytes hasta 300
    ax.set_yticklabels([str(i) for i in range(0, 210, 10)])
    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3, column=1, padx=5, pady=5, sticky="nsew", columnspan=2)


     
    
    # Configurar el grid para que las filas y columnas se expandan con la ventana
    for i in range(6):
        ventana.grid_rowconfigure(i, weight=1)
    for i in range(3):
        ventana.grid_columnconfigure(i, weight=1)
    
    # Actualizar
    def actualizar_info(txt_red, txt_aplicaciones):
    
    # Actualizar la información de actividad de red y graficos cpu y memoria
     # Obtener la información de actividad de red
       info_red = obtener_info_red()
       print("Información de actividad de red:", info_red)  # Imprimir información en la consola para verificar

       txt_red.config(state=tk.NORMAL)  # Habilitar el widget para edición
       txt_red.delete('1.0', tk.END)     # Eliminar el contenido actual
       txt_red.insert(tk.END, info_red)  # Insertar el nuevo contenido
       txt_red.config(state=tk.DISABLED)  # Deshabilitar el widget para evitar la edición

       info_aplicaciones = obtener_info_aplicaciones()  # Aquí deberías obtener la información de las aplicaciones instaladas
       print("Información de aplicaciones instaladas:", info_aplicaciones)  # Imprimir información en la consola para verificar
       txt_aplicaciones.config(state=tk.NORMAL)  # Habilitar el widget para edición
       txt_aplicaciones.delete('1.0', tk.END)     # Eliminar el contenido actual
       txt_aplicaciones.insert(tk.END, info_aplicaciones)  # Insertar el nuevo contenido
       txt_aplicaciones.config(state=tk.DISABLED)  # Deshabilitar el widget para evitar la ediciónn

# Llamada a la función actualizar_info
    def cambiar_tema(ventana, tema, color_fondo):
        ventana.set_theme(tema)
        ventana.configure(background=color_fondo)
    
    
# Crear el menú
    menu_bar = tk.Menu(ventana)
    ventana.config(menu=menu_bar)
    
# Menú "Configuración" /
    config_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Configuración", menu=config_menu)

    # submenu cambiar tema: Configuracion/
    visualizacion_menu = tk.Menu(config_menu, tearoff=0)
    config_menu.add_cascade(label="Cambiar tema", menu=visualizacion_menu)
    config_menu.add_separator()
    visualizacion_menu.add_command(label="Azul", command=lambda: cambiar_tema(ventana, "clam", "#A6DEE8"))
    visualizacion_menu.add_separator()
    visualizacion_menu.add_command(label="Verde", command=lambda: cambiar_tema(ventana, "clearlooks", "#C9ECD8"))
    visualizacion_menu.add_separator()
    visualizacion_menu.add_command(label="Morado", command=lambda: cambiar_tema(ventana, "radiance", "#E2B8F3"))  

    # Submenú "Redimensionar": configuración/redimensionar
    redimensionar_menu = tk.Menu(config_menu, tearoff=0)
    config_menu.add_cascade(label="Redimensionar", menu=redimensionar_menu)
   
    # Submenu: configuración/redimensionar/equilibrado vs personalizado
    redimensionar_menu.add_command(label="Equilibrado", command=lambda: ventana.geometry("960x540"))
    redimensionar_menu.add_separator()
    redimensionar_menu.add_command(label="Personalizado", command=lambda: ventana.geometry("1280x720"))


# Menú "Acciones" /
    consulta_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Acciones", menu=consulta_menu)
    consulta_menu.add_command(label="Actualizar paquetes", command=lambda: actualizar_info(txt_red, txt_aplicaciones))
    consulta_menu.add_separator()
    consulta_menu.add_command(label="Consultar Procesos", command=mostrar_procesos)
    consulta_menu.add_separator()

    # Submenú "Reiniciar servicios": acciones/reiniciar servicios
    reiniciar_menu = tk.Menu(consulta_menu, tearoff=0)
    consulta_menu.add_cascade(label="Reiniciar servicios", menu=reiniciar_menu)
    reiniciar_menu.add_command(label="Apache", command=reiniciar_apache)
    reiniciar_menu.add_command(label="MySQL", command=reiniciar_mysql)

    
# Menu ayuda /
    ayuda_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Ayuda", menu=ayuda_menu)
    # Submenú /ayuda/versión
    ayuda_menu.add_command(label="Versión", command=lambda: mostrar_version())
    ayuda_menu.add_separator()
    # Ayuda/salir
    ayuda_menu.add_command(label="Salir", command=ventana.destroy)
    

# Loop principal de la ventana
    ventana.mainloop()



 # Función para verificar las credenciales
def verificar_credenciales(username, password):
    # Verificar si el nombre de usuario y la contraseña coinciden con los valores de entorno
    if (username == os.getenv("USUARIO_ARGOS1") and password == os.getenv("CONTRASENA_ARGOS1")) or \
       (username == os.getenv("USUARIO_ARGOS2") and password == os.getenv("CONTRASENA_ARGOS2")):
        return True
    else:
        return False

# Función para iniciar sesión
def iniciar_sesion():
    # Obtener los datos ingresados por el usuario
    username = entry_usuario.get()
    password = entry_contraseña.get()
    
    # Verificar las credenciales
    if verificar_credenciales(username, password):
        lbl_estado.config(text="Acceso concedido")
        # Si se concede el acceso, iniciar la aplicación principal
        crear_interfaz()
    else:
        lbl_estado.config(text="Acceso denegado")
        # Cerrar la ventana automáticamente después de mostrar el mensaje de acceso denegado
        ventana_inicio.destroy

# Función para cerrar la ventana de inicio de sesión
def cerrar_ventana_inicio():
    ventana_inicio.destroy()
# Detener la ejecución del script al cerrar la ventana de inicio de sesión
    sys.exit(0)

# Crear la interfaz al ejecutar el script
if __name__ == "__main__":
    # Código para la ventana de inicio de sesión
    ventana_inicio = tk.Tk()
    ventana_inicio.title("Inicio de sesión")
    # Configurar el color de fondo
    ventana_inicio.configure(background="#E2B8F3")
    # Crear etiquetas y campos de entrada de texto para el nombre de usuario y la contraseña
    lbl_usuario = ttk.Label(ventana_inicio, text="Usuario:")
    lbl_usuario.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_usuario = ttk.Entry(ventana_inicio)
    entry_usuario.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    lbl_contraseña = ttk.Label(ventana_inicio, text="Contraseña:")
    lbl_contraseña.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_contraseña = ttk.Entry(ventana_inicio, show="*")
    entry_contraseña.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Botón para iniciar sesión
    btn_ingresar = ttk.Button(ventana_inicio, text="Ingresar", command=iniciar_sesion)
    btn_ingresar.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    # Etiqueta para mostrar el estado del inicio de sesión
    lbl_estado = ttk.Label(ventana_inicio, text="")
    lbl_estado.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    # Configurar la acción al cerrar la ventana
    ventana_inicio.protocol("WM_DELETE_WINDOW", cerrar_ventana_inicio)
    ventana_inicio.mainloop()

if __name__ == "__main__":
    crear_interfaz()