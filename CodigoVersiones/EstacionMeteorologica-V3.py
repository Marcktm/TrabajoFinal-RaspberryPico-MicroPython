from machine import Pin, I2C
from utime import sleep
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from dht import DHT11
import _thread
import machine
from ssd1306 import SSD1306_I2C
import framebuf


dht11_sensor = DHT11(Pin(28, Pin.IN))
dht11_sensor.measure()
temp = dht11_sensor.temperature()
hum = dht11_sensor.humidity()

LED_externo = Pin(15, Pin.OUT)
Buzz = Pin(14, Pin.OUT)
tim = machine.Timer()

pulsador = Pin(16, Pin.IN, Pin.PULL_DOWN)

scl = Pin(1)
sda = Pin(0)
freq = 400000

i2c = I2C(0,sda=sda,scl=scl,freq=freq)

I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

#Congigiracion-SensorPir

sensor_pir = Pin(21, Pin.IN, Pin.PULL_DOWN)

#OLED-Configuración

i2c2 = I2C(1,sda=Pin(26), scl=Pin(27))
oled = SSD1306_I2C(128, 64, i2c2)

#Defino-funcionParaAbrirImagen-PBM("LOGO")

def open_pbm(ruta_i):
    doc = open(ruta_i,"rb")
    doc.readline()
    posXY = doc.readline()
    x = int(posXY.split()[0])
    y = int(posXY.split()[1])
    logo = bytearray(doc.read())
    doc.close()
    return framebuf.FrameBuffer(logo , x, y, framebuf.MONO_HLSB)

a=1
b=0

#INTERRUPCION_PARA_EL_BUZZER: Lo apaga
def offBuzz(pin):
    global a
    a = 0
    Buzz.value(0)
           
pulsador.irq(offBuzz, machine.Pin.IRQ_RISING)


#FUNCION_QUE_ACTIVA_EL_BUZZER_DESPUES_DEL_TIMER
def tick(timer):
    global a
    a = 1
    
#Se usa el segundo hilo para que el display OLED cambie de mensaje     
def estadoOled():
    while True:
        if sensor_pir.value() == 1:
            oled.fill(0)
            oled.blit(open_pbm("images/micropython-1.pbm"), 35, 5)
            oled.show()
            sleep(10)
        else:
            oled.fill(0)
            oled.text('NO HAY NADIE', 15, 30)
            oled.text('CERCA', 40, 40)
            oled.show()
        
_thread.start_new_thread(estadoOled, ())
    
       
while True:
    sleep(2)
        
    lcd.clear() 
    lcd.move_to(0,0) 
    
    dht11_sensor.measure()
    temp = dht11_sensor.temperature()
    hum = dht11_sensor.humidity()
    
    Text = 'Temperatura:' + str(temp)  +chr(223)+"C" + 'Humedad:' + str(hum) + "%"
    lcd.putstr(Text) 
    sleep(5)
    
    if temp >= 30:
        LED_externo.value(1)
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr("Cuidado: ALTA   TEMPERATURA")
        sleep(3)
        lcd.clear()
    else:
        LED_externo.value(0)
        
    if hum >= 70:
        if a == 0 :
            tim.init(period=10000, mode=machine.Timer.PERIODIC, callback=tick)
        Buzz.value(a)
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr("Cuidado: HUMEDAD RELATIVA > 70% ")
        sleep(3)
    else:
        Buzz.value(0)
    
