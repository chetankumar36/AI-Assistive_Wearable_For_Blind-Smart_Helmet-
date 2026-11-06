from time import sleep
from gpiozero import DigitalInputDevice
ldr_pin = 21


ldr = DigitalInputDevice(pin = ldr_pin)

sleep(1)

def read_ir(ldr):
    return ldr.is_active
while True:
    val = read_ir(ldr)
    if val:
        print("Night")
    else:
        print("Day")
    sleep(0.2)


    