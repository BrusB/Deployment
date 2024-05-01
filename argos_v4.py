import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk
from tkinter import ttk
import pkg_resources
from ttkthemes import ThemedTk
from tkinter import Toplevel, Text, Scrollbar
import subprocess


# Función para obtener información sobre los discos
def obtener_info_discos():
    discos = psutil.disk_partitions()
    info_discos = ""
    for disco in discos:
        info_discos += f"Disco: {disco.device}\n"
        info_discos += f"  Punto de montaje: {disco.mountpoint}\n"
        info_discos += f"  Tipo: {disco.fstype}\n"

        # Obtener información sobre el uso del disco
        uso_disco = psutil.disk_usage(disco.mountpoint)
        info_discos += f"  Tamaño total: {bytes_to_gb(uso_disco.total)} GB\n"
        info_discos += f"  Espacio utilizado: {bytes_to_gb(uso_disco.used)} GB\n"
        info_discos += f"  Espacio libre: {bytes_to_gb(uso_disco.free)} GB\n\n"
    return info_discos

# Función para obtener información sobre el rendimiento del sistema
def obtener_info_rendimiento():
    cpu_percent = psutil.cpu_percent()
    mem_percent = psutil.virtual_memory().percent
    return cpu_percent, mem_percent

# Función para obtener información sobre las aplicaciones instaladas
def obtener_info_aplicaciones():
    aplicaciones = ""
    try:
        # Obtener la lista de paquetes instalados
        paquetes = [p.key for p in pkg_resources.working_set]
        for paquete in paquetes:
            aplicaciones += f"- {paquete}\n"
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

# Función para convertir bytes a gigabytes
def bytes_to_gb(bytes):
    return round(bytes / (1024 ** 3), 2)

# Función para convertir bytes a megabytes
def bytes_to_mb(bytes):
    return round(bytes / (1024 ** 2), 2)

# Función para mostrar la versión
def mostrar_version():
    tk.messagebox.showinfo("Versión", "Versión 1.3 beta")



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
def mostrar_procesos():
    # Crear una ventana emergente
    ventana_procesos = Toplevel()
    ventana_procesos.title("Procesos en Ejecución")

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
   
# Función principal para crear la interfaz de usuario
def crear_interfaz():
    # Configuración de la ventana principal
    ventana = ThemedTk(theme="radiance")  # Puedes cambiar el tema a tu preferencia

    # Cambiar el tipo de letra del título de la ventana
    ventana.title("@RGOS")
    # fondo
    ventana.configure(background="#E2B8F3")
    
    # Tamaño y posición de la ventana
    ancho_ventana = 1024  # Ajusta el ancho de la ventana según tus necesidades
    alto_ventana = 600     # Ajusta el alto de la ventana según tus necesidades
    x_ventana = (ventana.winfo_screenwidth() // 2) - (ancho_ventana // 2)
    y_ventana = (ventana.winfo_screenheight() // 2) - (alto_ventana // 2)
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x_ventana}+{y_ventana}")

 # Configura la grilla para que el canvas se ajuste con el tamaño de la ventana
    ventana.grid_columnconfigure(2, weight=1)
    ventana.grid_rowconfigure(0, weight=1)

# Función para obtener el porcentaje de uso de CPU y memoria
    def obtener_info_rendimiento():
       cpu_percent = psutil.cpu_percent()
       mem_percent = psutil.virtual_memory().percent
       return cpu_percent, mem_percent
    cpu_percent, mem_percent = obtener_info_rendimiento()

 # Gráfico circular para mostrar uso de CPU y memoria
    # Especificar los colores para CPU y Memoria
    color_cpu = '#8195F8'  # Color para la sección de CPU
    color_memoria = '#FBFB78'  # Color para la sección de Memoria
    fig2 = plt.Figure(figsize=(4, 3), dpi=100)  # tamaño de la figura
    ax2 = fig2.add_subplot(111)
    ax2.pie([cpu_percent, mem_percent], labels=['CPU', 'Memoria'], autopct='%1.1f%%', startangle=140, colors=[color_cpu, color_memoria])
    fig2.tight_layout()  # Ajustar el diseño de la figura
    canvas2 = FigureCanvasTkAgg(fig2, master=ventana)
    canvas2.draw()
    canvas2.get_tk_widget().grid(row=0, column=2, rowspan=2, padx=0, pady=(40,5), sticky="nsew") # Aplicar padding diferente para la parte superior e inferior

    cpu_percent, mem_percent = obtener_info_rendimiento()
    txt_rendimiento = tk.Text(ventana, height=20, width=50)
    txt_rendimiento.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")  # Agregar esta línea para posicionar el widget de texo
    lbl_grafico = ttk.Label(ventana, text="USO CPU Y MEMORIA")
    lbl_grafico.grid(row=0, column=2, sticky="w", padx=10, pady=5)  # Mover este grid a la misma columna que el gráfico circular


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

    # Configurar la expansión de la ventana
    ventana.grid_rowconfigure(3, weight=1)
    ventana.grid_columnconfigure(0, weight=1)

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

    # Crear un widget de texto para mostrar mensajes
    lbl_estado_grafico = ttk.Label(ventana, text="")
    lbl_estado_grafico.grid(row=2, column=2, sticky="w", padx=10, pady=5)
    # Función para actualizar el gráfico circular con los nuevos datos de uso de CPU y memoria
    def actualizar_grafico():
         color_cpu = '#8195F8'  # Color para la sección de CPU
         color_memoria = '#FBFB78'  # Color para la sección de Memoria
         cpu_percent, mem_percent = obtener_info_rendimiento()
         print("Uso de CPU:", cpu_percent)  # Imprimir el uso de CPU
         print("Uso de memoria:", mem_percent)  # Imprimir el uso de memoria
         lbl_estado_grafico.config(text="Borrando el gráfico...")  # Actualizar el mensaje
         ax2.clear()  # Limpiar el gráfico anterior
         
         ax2.pie(obtener_info_rendimiento(), labels=['CPU', 'Memoria'], autopct='%1.1f%%', startangle=140, colors=[color_cpu, color_memoria])
         fig2.tight_layout()  # Ajustar el diseño de la figura
         canvas2.draw()  # Dibujar el nuevo gráfico en el lienzo
         lbl_estado_grafico.config(text="Gráfico actualizado")  # Actualizar el mensaje nuevamente después de dibujar el nuevo gráfico
    
    # Función para actualizar la información mostrada
    def actualizar_info(txt_discos, txt_rendimiento, txt_aplicaciones, txt_red):
     # Actualizar la información de discos
     txt_discos.config(state=tk.NORMAL)
     txt_discos.delete('1.0', tk.END)
     txt_discos.insert(tk.END, obtener_info_discos())
     txt_discos.config(state=tk.DISABLED)

     # Actualizar la información de rendimiento
     txt_rendimiento.config(state=tk.NORMAL)
     txt_rendimiento.delete('1.0', tk.END)
     txt_rendimiento.insert(tk.END, obtener_info_rendimiento())
     txt_rendimiento.config(state=tk.DISABLED)

     # Actualizar la información de aplicaciones instaladas
     txt_aplicaciones.config(state=tk.NORMAL)
     txt_aplicaciones.delete('1.0', tk.END)
     txt_aplicaciones.insert(tk.END, obtener_info_aplicaciones())
     txt_aplicaciones.config(state=tk.DISABLED)

     # Actualizar la información de actividad de red
     txt_red.config(state=tk.NORMAL)
     txt_red.delete('1.0', tk.END)
     txt_red.insert(tk.END, obtener_info_red())
     txt_red.config(state=tk.DISABLED)
     # Actualizar el gráfico circular
     actualizar_grafico()    
    
    # Configurar el grid para que las filas y columnas se expandan con la ventana
    for i in range(6):
        ventana.grid_rowconfigure(i, weight=1)
    for i in range(3):
        ventana.grid_columnconfigure(i, weight=1)

    # Crear el menú
    menu_bar = tk.Menu(ventana)
    ventana.config(menu=menu_bar)

    # Menú "Consulta"
    consulta_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Consulta", menu=consulta_menu)
    consulta_menu.add_command(label="Actualizar", command=lambda: actualizar_info(txt_discos, txt_rendimiento, txt_aplicaciones, txt_red))
    consulta_menu.add_separator()
    # Agregar la opción en el menú Consulta
    consulta_menu.add_command(label="Consultar Procesos", command=mostrar_procesos)
    consulta_menu.add_separator()
    consulta_menu.add_command(label="Salir", command=ventana.quit)

    # Menú "Configuración"
    config_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Configuración", menu=config_menu)
    # Agregar opciones de configuración aquí si es necesario

    ayuda_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Ayuda", menu=ayuda_menu)
    ayuda_menu.add_command(label="Versión", command=lambda: mostrar_version())
    ayuda_menu.add_separator()
    ayuda_menu.add_command(label="Salir", command=ventana.quit)



# Loop principal de la ventana
    ventana.mainloop()

# Crear la interfaz al ejecutar el script
if __name__ == "__main__":
    crear_interfaz()
