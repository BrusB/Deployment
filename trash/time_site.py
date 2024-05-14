# fecha_html.py

import datetime

# Obtener la fecha y hora actual
fecha_actual = datetime.datetime.now()

# Formatear la fecha y hora
fecha_formateada = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")

# Crear el contenido HTML con la fecha
contenido_html = f"<html><head><title>Fecha actual</title></head><body><h1>Fecha y hora actual:</h1><p>{fecha_formateada}</p></body></html>"

# Escribir el contenido en un archivo HTML
with open("fecha_actual.html", "w") as file:
    file.write(contenido_html)
