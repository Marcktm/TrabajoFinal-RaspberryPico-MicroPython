from machine import Pin, I2C
from utime import sleep
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from dht import DHT11

dht11_sensor = DHT11(Pin(28, Pin.IN))
dht11_sensor.measure()
temp = dht11_sensor.temperature()
hum = dht11_sensor.humidity()

LED_externo = Pin(15, Pin.OUT)
LED_externo2 = Pin(14, Pin.OUT)

scl = Pin(1)
sda = Pin(0)
freq = 400000

i2c = I2C(0,sda=sda,scl=scl,freq=freq)

I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
while True:
    sleep(2)
    lcd.clear() # Borra cualquier caracter previo que exista
    lcd.move_to(0,0) # Posiciona el cursor en el primer renglón y en la primera columna
    
    dht11_sensor.measure()
    temp = dht11_sensor.temperature()
    hum = dht11_sensor.humidity()
    
    if temp >= 30:
        LED_externo.value(1)
    else:
        LED_externo.value(0)
        
    if hum >= 70:
        LED_externo2.value(1)
    else:
        LED_externo2.value(0)
        
    
    Text = 'Temperatura:' + str(temp)  +chr(223)+"C" + 'Humedad:' + str(hum) + "%"
    lcd.putstr(Text) # Escribir en la pantalla
    sleep(5)