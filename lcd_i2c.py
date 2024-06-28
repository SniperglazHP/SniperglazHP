from machine import Pin, I2C
from time import sleep
from pico_i2c_lcd import I2cLcd
from machine import SoftI2C
import random
import network, urequests, machine

I2C_DDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

ssid = "UNIFI-ITSA"
password = ""
wlan = network.WLAN(network.STA_IF)
print(wlan.active(True))
wlan.connect(ssid, password)
while not wlan.isconnected():
    pass

url = "https://api.thingspeak.com/update?api_key=T3KABTQMOAA9YDW2"

# Configuración del I2C
i2c = SoftI2C(sda=Pin(4), scl=Pin(5), freq=40000)

# Inicializar el LCD
lcd = I2cLcd(i2c, I2C_DDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Configuración del botón
button = Pin(18, Pin.IN, Pin.PULL_UP)

# Definición de caracteres personalizados
player_char = [0x0E, 0x0A, 0x0E, 0x04, 0x0E, 0x15, 0x0A, 0x0A]  # Jugador
target_char = [0x0E, 0x0A, 0x0E, 0x04, 0x0E, 0x0A, 0x0E, 0x1F]  # Objetivo

# Cargar caracteres personalizados en el LCD
lcd.custom_char(0, bytearray(player_char))
lcd.custom_char(1, bytearray(target_char))

# Variables de contadores
aciertos = 0
fallos = 0
intentos = 0  # Añadir contador de intentos

def start_game():
    global aciertos, fallos, intentos
    lcd.clear()
    lcd.putstr("Atrápalo")
    sleep(1)
    lcd.clear()
    cursor_position = 0
    target_position = random.randint(0, 15)
    lcd.move_to(target_position, 1)
    lcd.putchar(chr(1))  # Mostrar el objetivo
    intentos += 1

    while True:
        if button.value() == 0:
            if cursor_position == target_position:
                aciertos += 1
                lcd.clear()
                lcd.putstr("Ganaste")
                break
            else:
                fallos += 1
                lcd.clear()
                lcd.putstr("Perdiste")
                break
        lcd.move_to(cursor_position, 0)
        lcd.putchar(chr(0))  # Mostrar el jugador
        sleep(0.2)
        lcd.move_to(cursor_position, 0)
        lcd.putstr(' ')  # Limpiar la posición anterior del jugador
        cursor_position = (cursor_position + 1) % 16

    sleep(2)
    lcd.clear()
    lcd.putstr(f"Fallos: {fallos}")
    lcd.move_to(0, 1)
    lcd.putstr(f"Aciertos: {aciertos}")
    print(str(fallos) + "-" + str(aciertos))
    #f"{url}&field3={fallos}&field2={aciertos}"
    respuesta = urequests.get(url + "&field3=" + str(fallos) + "&field2=" + str(aciertos))
    respuesta.close()
    sleep(3)

def main():
    global intentos
    while intentos < 5:  # Terminar después de 5 intentos
        start_game()
        sleep(2)
    
    # Mostrar mensaje de fin de juego
    lcd.clear()
    lcd.putstr("Fin del Juego")
    sleep(2)
    lcd.clear()
    lcd.putstr(f"T Fallos: {fallos}")
    lcd.move_to(0, 1)
    lcd.putstr(f"T Aciertos: {aciertos}")
    print("Juego terminado.")
    print("T Fallos:", fallos)
    print("T Aciertos:", aciertos)

main()
