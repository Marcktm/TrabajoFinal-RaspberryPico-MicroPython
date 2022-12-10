from machine import Pin, I2C
from utime import sleep
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from dht import DHT11
import _thread

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

a=1

def offBuzz(pin):
    global a
    a = 0
    Buzz.value(0)

pulsador.irq(offBuzz, machine.Pin.IRQ_RISING)
    
def tick(timer):
    global a
    a = 1
       
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
        
        
