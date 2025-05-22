import funciones
import pandas as pd
import os
from sqlalchemy import create_engine

# Crear un DataFrame vacío para almacenar todas las facturas
df = pd.DataFrame()

# Recorrer todas las carpetas dentro de la carpeta "facturas"
for carpeta in sorted(os.listdir("./facturas")):
    ruta_carpeta = os.path.join("./facturas/", carpeta)

    # Recorrer todos los archivos dentro de la carpeta
    for archivo in os.listdir(ruta_carpeta):
        ruta_pdf = os.path.join(ruta_carpeta, archivo)

        print(f"📄 Procesando factura: {ruta_pdf}")

        # Extraer texto de la factura
        texto_no_estructurado = funciones.extraer_texto_pdf(ruta_pdf)

        # Estructurar el texto de la factura
        texto_estructurado = funciones.estructurar_texto(texto_no_estructurado)

        # Convertir texto estructurado en dataframe
        df_factura = funciones.csv_a_dataframe(texto_estructurado)

        # Anexar el dataframe de la factura al dataframe general
        df = pd.concat([df, df_factura], ignore_index=True)

    # Si la moneda es "dolares" convertir a euros multiplicando por 0,9243
    #df.loc[df["moneda"] == "dolares", "importe"] *= 0.9243

    # Eliminar las columnas no esenciales
    df = df.iloc[:, 0:4]

# Guardar el DataFrame final en una bbdd sqlite
# Crear una conexión a la base de datos SQLite
engine = create_engine("sqlite:///facturas.db")

# Guardar el DataFrame final en una bbdd sqlite, añadiendo los datos en lugar de reemplazarlos
df.to_sql("facturas", engine, if_exists="append", index=False)

# Cerrar la conexión a la base de datos
engine.dispose()

print("Proceso de extracción y estructuración de facturas completado exitosamente.")
print("Datos guardados en la base de datos 'facturas.db'.")
