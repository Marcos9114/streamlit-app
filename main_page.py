import streamlit as st
import pandas as pd
import openpyxl

# Función para cargar y procesar datos
@st.cache_data
def cargar_datos(ruta_archivo):
    datos = pd.read_excel(ruta_archivo)
    datos = datos.dropna(subset=['latitud'])

    # Convertir las columnas 'latitud' y 'longitud' a valores numéricos
    datos['latitud'] = pd.to_numeric(datos['latitud'], errors='coerce')
    datos['longitud'] = pd.to_numeric(datos['longitud'], errors='coerce')

    # Eliminar filas con valores nulos en las columnas 'latitud' o 'longitud'
    datos = datos.dropna(subset=['latitud', 'longitud'])
    datos['size'] = datos['POTENCIA'] / 10

    return datos

# Ruta al archivo Excel
ruta_archivo = '/workspaces/streamlit-app/PLANILLA FACTIBILIDADES desde 2020 v2.xlsx'

# Cargar los datos utilizando la función cacheada
datos = cargar_datos(ruta_archivo)

# Agregar un slider para filtrar por POTENCIA
min_potencia, max_potencia = int(datos['POTENCIA'].min()), int(datos['POTENCIA'].max())
rango_potencia = st.slider(
    "Selecciona el rango de POTENCIA:",
    min_potencia,
    max_potencia,
    (min_potencia, max_potencia)
)

# Filtrar los datos según el rango de POTENCIA
datos_filtrados = datos[(datos['POTENCIA'] >= rango_potencia[0]) & (datos['POTENCIA'] <= rango_potencia[1])]

# Mostrar los datos filtrados
st.write("Datos filtrados según el rango de POTENCIA seleccionado:")
st.write(datos_filtrados)

# Mostrar el mapa con los datos filtrados
st.map(datos_filtrados, latitude="latitud", longitude="longitud", size="size")
