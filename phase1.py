import os
import glob
import time
from gpiozero import DigitalInputDevice
from RPLCD import *
from time import sleep
from RPLCD.i2c import CharLCD
import time

ldr_pin = 21


ldr = DigitalInputDevice(pin = ldr_pin)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True,
              backlight_enabled=True)
lcd.cursor_pos = (0, 0)


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f
    
def read_ldr(ldr):
    return ldr.is_active

while True:
    temperature_celsius, temperature_fahrenheit = read_temp()
    print(f'Temperature: {temperature_celsius:.2f} °C')
    #print(f'Temperature: {temperature_fahrenheit:.2f} °F')
    val = read_ldr(ldr)
    if val:
        print("Night")
        status = "Night"
    else:
        print("Day")
        status = "Day"
    print('')

    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("Temp:" + str(temperature_celsius) + "C")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("Status:" + status)