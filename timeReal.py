from flask import Flask, render_template, jsonify
import mysql.connector
import plotly.graph_objs as go
import plotly.io as pio
from datetime import datetime

app = Flask(__name__)

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_ejercicios"  # Nombre de la base de datos correcto
    )

# Función para obtener sesiones por usuario
def obtener_sesiones_por_usuario():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT u.Nombre, COUNT(s.idSesion) AS Total_Sesiones
        FROM Usuarios u
        JOIN Sesiones s ON u.idUsuario = s.idUsuario
        GROUP BY u.idUsuario
    """)
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    return resultados

# Función para obtener la duración promedio de las sesiones por usuario
def obtener_duracion_promedio_por_usuario():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT u.Nombre, AVG(s.Duracion) AS Duracion_Promedio
        FROM Usuarios u
        JOIN Sesiones s ON u.idUsuario = s.idUsuario
        GROUP BY u.idUsuario
    """)
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    return resultados

# Función para obtener la mejora de fuerza a lo largo del tiempo
def obtener_mejora_fuerza():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT u.Nombre, p.Fecha_calculo, p.Mejora_fuerza
        FROM Progreso p
        JOIN Usuarios u ON p.idUsuario = u.idUsuario
    """)
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    return resultados

# Función para obtener movilidad horizontal, vertical y diagonal promedio
def obtener_movilidades_promedio():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT AVG(p.Movilidad_horizontal) AS Movilidad_Horizontal, 
               AVG(p.Movilidad_vertical) AS Movilidad_Vertical,
               AVG(p.Precision_diagonal) AS Movilidad_Diagonal
        FROM Progreso p
    """)
    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    return resultado

@app.route('/')
def index():
    return render_template('timeReal.html')

@app.route('/datos_grafico', methods=['GET'])
def datos_grafico():
    # Obtener datos de las funciones
    sesiones_usuario = obtener_sesiones_por_usuario()
    duracion_promedio_usuario = obtener_duracion_promedio_por_usuario()
    mejora_fuerza = obtener_mejora_fuerza()
    movilidades_promedio = obtener_movilidades_promedio()

    # Datos para cada gráfico

    # Gráfico de cantidad de sesiones por usuario
    nombres_usuario = [row[0] for row in sesiones_usuario]
    total_sesiones = [row[1] for row in sesiones_usuario]

    # Gráfico de duración promedio de las sesiones por usuario
    duracion_promedio = [row[1] for row in duracion_promedio_usuario]

    # Gráfico de mejora de fuerza a lo largo del tiempo
    fechas = [row[1] for row in mejora_fuerza]
    mejora_fuerza_valores = [row[2] for row in mejora_fuerza]
    nombres_fuerza = list(set([row[0] for row in mejora_fuerza]))

    # Gráfico de movilidad (horizontal, vertical, diagonal)
    movilidad_horizontal = movilidades_promedio[0]
    movilidad_vertical = movilidades_promedio[1]
    movilidad_diagonal = movilidades_promedio[2]

    # Gráfico de barras para sesiones por usuario
    trace1 = go.Bar(x=nombres_usuario, y=total_sesiones, name='Total de Sesiones por Usuario')

    # Gráfico de barras para duración promedio de sesiones
    trace2 = go.Bar(x=nombres_usuario, y=duracion_promedio, name='Duración Promedio por Usuario')

    # Gráfico de línea para mejora de fuerza a lo largo del tiempo
    trace3 = go.Scatter(x=fechas, y=mejora_fuerza_valores, mode='lines', name='Mejora de Fuerza')

    # Gráfico de barras para movilidad
    trace4 = go.Bar(x=['Movilidad Horizontal', 'Movilidad Vertical', 'Movilidad Diagonal'], 
                    y=[movilidad_horizontal, movilidad_vertical, movilidad_diagonal], name='Movilidad Promedio')

    layout = go.Layout(
        title=f'Estadísticas de Jugadores - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        xaxis_title='Usuarios / Fechas / Movilidad',
        yaxis_title='Valor',
        barmode='group',  # Para mostrar las barras por grupo
        margin=dict(l=40, r=40, t=40, b=40)
    )

    fig = go.Figure(data=[trace1, trace2, trace3, trace4], layout=layout)
    graph_json = pio.to_json(fig)

    return jsonify(graph_json)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
