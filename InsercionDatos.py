from machine import Pin, ADC
import ujson
import time
import urequests as requests
import sys
import os

# Detectar el tipo de tarjeta
class Board:
    class BoardType:
        PICO_W = 'Raspberry Pi Pico W'
        PICO = 'Raspberry Pi Pico'
        RP2040 = 'RP2040'
        ESP8266 = 'ESP8266'
        ESP32 = 'ESP32'
        UNKNOWN = 'Unknown'

    def __init__(self):
        self.type = self.detect_board_type()

    def detect_board_type(self):
        sysname = os.uname().sysname.lower()
        machine_name = os.uname().machine.lower()
        if sysname == 'rp2' and 'pico w' in machine_name:
            return self.BoardType.PICO_W
        elif sysname == 'rp2' and 'pico' in machine_name:
            return self.BoardType.PICO
        elif sysname == 'rp2' and 'rp2040' in machine_name:
            return self.BoardType.RP2040
        elif sysname == 'esp8266':
            return self.BoardType.ESP8266
        elif sysname == 'esp32' and 'esp32' in machine_name:
            return self.BoardType.ESP32
        else:
            return self.BoardType.UNKNOWN

BOARD_TYPE = Board().type
print("Tarjeta Detectada: " + BOARD_TYPE)

if BOARD_TYPE == Board.BoardType.ESP32:
    led_verde = Pin(21, Pin.OUT)
    led_rojo = Pin(19, Pin.OUT)
    joysticks = [
        {"x": ADC(Pin(34)), "y": ADC(Pin(35)), "sw": Pin(26, Pin.IN, Pin.PULL_UP)},
        {"x": ADC(Pin(36)), "y": ADC(Pin(39)), "sw": Pin(25, Pin.IN, Pin.PULL_UP)},
        {"x": ADC(Pin(32)), "y": ADC(Pin(33)), "sw": Pin(27, Pin.IN, Pin.PULL_UP)},
        {"x": ADC(Pin(14)), "y": ADC(Pin(12)), "sw": Pin(13, Pin.IN, Pin.PULL_UP)}
    ]

    for joystick in joysticks:
        joystick["x"].atten(ADC.ATTN_11DB)
        joystick["y"].atten(ADC.ATTN_11DB)

    CENTRO_MIN = 1600
    CENTRO_MAX = 2000

    url = "http://192.168.37.114/InsercionDatos.php"

    def map_value(val, in_min, in_max, out_min, out_max):
        return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def leer_joystick(joystick):
        x_val = joystick["x"].read()
        y_val = joystick["y"].read()
        sw_val = joystick["sw"].value()

        if x_val < CENTRO_MIN:
            x_nivel = map_value(x_val, 0, CENTRO_MIN, -10, 0)
        elif x_val > CENTRO_MAX:
            x_nivel = map_value(x_val, CENTRO_MAX, 4095, 0, 10)
        else:
            x_nivel = 0

        if y_val < CENTRO_MIN:
            y_nivel = map_value(y_val, 0, CENTRO_MIN, -10, 0)
        elif y_val > CENTRO_MAX:
            y_nivel = map_value(y_val, CENTRO_MAX, 4095, 0, 10)
        else:
            y_nivel = 0

        x_direccion = "Centro" if x_nivel == 0 else ("Izquierda" if x_nivel < 0 else "Derecha")
        y_direccion = "Centro" if y_nivel == 0 else ("Arriba" if y_nivel < 0 else "Abajo")
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

        return {
            "x_val": x_val,
            "y_val": y_val,
            "x_nivel": x_nivel,
            "y_nivel": y_nivel,
            "x_direccion": x_direccion,
            "y_direccion": y_direccion,
            "diagonal": diagonal,
            "boton": "Presionado" if sw_val == 0 else "No presionado"
        }

    while True:
        datos_joysticks = []
        for i, joystick in enumerate(joysticks):
            datos = leer_joystick(joystick)
            datos["joystick_id"] = i + 1
            datos_joysticks.append(datos)

        data_json = {
            "joysticks": datos_joysticks,
            "timestamp": int(time.time())
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=ujson.dumps(data_json), headers=headers)
        print("Respuesta del servidor:", response.text)

        led_verde.on()
        led_rojo.off()
        time.sleep(0.1)

        if False:
            led_verde.off()
            led_rojo.on()
            break
