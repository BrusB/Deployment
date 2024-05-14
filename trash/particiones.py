import psutil
import subprocess
import time

# Función para obtener información de discos
def obtener_info_discos():
    discos = psutil.disk_partitions()
    info_discos = ""
    for disco in discos:
        info_discos += f"Disco: {disco.device}<br>"
        info_discos += f"  Punto de montaje: {disco.mountpoint}<br>"
        info_discos += f"  Tipo: {disco.fstype}<br>"

        # Obtener información sobre el uso del disco
        uso_disco = psutil.disk_usage(disco.mountpoint)
        info_discos += f"  Tamaño total: {bytes_to_gb(uso_disco.total)} GB<br>"
        info_discos += f"  Espacio utilizado: {bytes_to_gb(uso_disco.used)} GB<br>"
        info_discos += f"  Espacio libre: {bytes_to_gb(uso_disco.free)} GB<br><br>"
    return info_discos

# Función para convertir bytes a gigabytes
def bytes_to_gb(bytes):
    return round(bytes / (1024 ** 3), 2)

# Función para generar el archivo HTML
def generar_html():
    html_template = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Información del Sistema</title>
    </head>
    <body>
        <h1>Información del Sistema</h1>
        <h2>Discos:</h2>
        {obtener_info_discos()}
    </body>
    </html>
    """
    with open("informacion_sistema.html", "w") as file:
        file.write(html_template)

# Generar el archivo HTML
generar_html()
print("Archivo HTML generado exitosamente.")
