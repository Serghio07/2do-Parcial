import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Configuración de la base de datos
db_config = {
    'user': 'root',       # Cambia esto por tu nombre de usuario MySQL
    'password': '',       # Cambia esto por tu contraseña MySQL
    'host': 'localhost',  # Cambia esto si tu servidor MySQL está en otra dirección
    'database': 'db_ejercicios'  # Cambia esto por el nombre de tu base de datos
}

# Crear la cadena de conexión con SQLAlchemy
connection_string = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"

# Crear el engine de SQLAlchemy
engine = create_engine(connection_string)

# Consulta SQL para leer los datos de la tabla Lecturas
query = """
SELECT 
    S.Fecha_sesion AS fecha,  -- Cambié la fuente de 'Fecha_sesion' a la tabla 'Sesiones'
    L.Direccion,
    L.Diagonal,
    L.Eje_x,
    L.Eje_y,
    L.Nivel_x,
    L.Nivel_y
FROM 
    Lecturas L
JOIN 
    Sesiones S ON L.idSesion = S.idSesion
JOIN 
    Usuarios U ON S.idUsuario = U.idUsuario
WHERE 
    U.idUsuario = %s  -- Filtrar por el idUsuario que desees
"""
# Puedes reemplazar el %s por un valor específico de idUsuario
user_id = 1  # Ejemplo de idUsuario, cámbialo según sea necesario
data = pd.read_sql(query, engine, params=(user_id,))

# Verificar el número total de registros
print(f'Número total de registros: {len(data)}')

# Mostrar todos los datos en consola sin truncar
pd.set_option('display.max_rows', None)  # Esto muestra todas las filas
print(data)

# Graficar los movimientos
plt.figure(figsize=(12, 8))

# Graficar las direcciones y niveles de movimiento
plt.plot(data['fecha'], data['Eje_x'], label='Eje X', color='blue')
plt.plot(data['fecha'], data['Eje_y'], label='Eje Y', color='orange')
plt.plot(data['fecha'], data['Nivel_x'], label='Nivel X', color='green')
plt.plot(data['fecha'], data['Nivel_y'], label='Nivel Y', color='red')

# Configuración del gráfico
plt.title(f'Movimientos del Joystick para Usuario {user_id}')
plt.xlabel('Fecha de Sesión')
plt.ylabel('Valores')
plt.legend()
plt.grid(True)
    
# Mostrar el gráfico
plt.show()
