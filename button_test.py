from gpiozero import Button
import time
from gpiozero import Buzzer

temp_button_pin = 20

temp_button = Button(temp_button_pin)


buzzer = Buzzer(16)

while True:
        if not temp_button.is_pressed:
            print("pressed")
            buzzer.on()
        else:
            print("not button pressed")
            buzzer.off()
        time.sleep(1)