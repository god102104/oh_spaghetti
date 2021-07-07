from gpiozero import LED
from time import sleep

green_led = LED(17)
green_led.on()
count = 0

while True:
    green_led.on()
    sleep(1)
    green_led.off()
