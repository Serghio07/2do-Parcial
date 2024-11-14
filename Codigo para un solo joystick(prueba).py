from machine import Pin, ADC
from time import sleep

# Configuración de los pines
vrx_pin = 34  # Pin para el eje X
vry_pin = 35  # Pin para el eje Y
sw_pin = 26   # Pin para el botón del joystick

# Configuración de los pines como entradas analógicas o digitales
vrx = ADC(Pin(vrx_pin))
vry = ADC(Pin(vry_pin))
sw = Pin(sw_pin, Pin.IN, Pin.PULL_UP)  # Configuración del botón con resistencia pull-up

# Configuración del ancho de bits para lectura
vrx.atten(ADC.ATTN_11DB)
vry.atten(ADC.ATTN_11DB)

# Rango ajustado para el centro del joystick
CENTRO_MIN = 1600
CENTRO_MAX = 2000

# Función de mapeo para obtener niveles proporcionales de precisión
def map_value(val, in_min, in_max, out_min, out_max):
    return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

while True:
    # Leer valores del joystick
    x_val = vrx.read()
    y_val = vry.read()
    sw_val = sw.value()  # 0 si está presionado, 1 si no lo está

    # Determinar niveles de movimiento en X e Y con mapeo proporcional
    if x_val < CENTRO_MIN:
        x_nivel = map_value(x_val, 0, CENTRO_MIN, -10, 0)  # Valores negativos para la izquierda
    elif x_val > CENTRO_MAX:
        x_nivel = map_value(x_val, CENTRO_MAX, 4095, 0, 10)  # Valores positivos para la derecha
    else:
        x_nivel = 0  # En el centro

    if y_val < CENTRO_MIN:
        y_nivel = map_value(y_val, 0, CENTRO_MIN, -10, 0)  # Valores negativos para arriba
    elif y_val > CENTRO_MAX:
        y_nivel = map_value(y_val, CENTRO_MAX, 4095, 0, 10)  # Valores positivos para abajo
    else:
        y_nivel = 0  # En el centro

    # Determinar la dirección del movimiento en base a los niveles mapeados
    x_direccion = "Centro" if x_nivel == 0 else ("Izquierda" if x_nivel < 0 else "Derecha")
    y_direccion = "Centro" if y_nivel == 0 else ("Arriba" if y_nivel < 0 else "Abajo")

    # Determinar la dirección de la diagonal
    diagonal = "No está en ninguna diagonal"
    if x_direccion != "Centro" and y_direccion != "Centro":
        if x_direccion == "Izquierda" and y_direccion == "Arriba":
            diagonal = "Diagonal arriba izquierda"
        elif x_direccion == "Derecha" and y_direccion == "Arriba":
            diagonal = "Diagonal arriba derecha"
        elif x_direccion == "Izquierda" and y_direccion == "Abajo":
            diagonal = "Diagonal abajo izquierda"
        elif x_direccion == "Derecha" and y_direccion == "Abajo":
            diagonal = "Diagonal abajo derecha"

    # Imprimir valores en la consola
    print("Eje X:", x_val, "Eje Y:", y_val, "Botón:", "Presionado" if sw_val == 0 else "No presionado")
    print("Nivel X:", x_nivel, "| Nivel Y:", y_nivel)
    print("Movimiento en X:", x_direccion, "| Movimiento en Y:", y_direccion)
    print("Dirección de la diagonal:", diagonal)

    sleep(0.1)  # Esperar un poco antes de la siguiente lectura

