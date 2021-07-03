from __future__ import print_function
import time
from pyA20.gpio import gpio as GPIO
from pyA20.gpio import port

def measure():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        start = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        stop = time.time()

    elapsed = stop-start
    distance = (elapsed * 34300)/2

    return distance

def measure_average():
    distance1=measure()
    time.sleep(0.1)
    distance2=measure()
    time.sleep(0.1)
    distance3=measure()
    distance = distance1 + distance2 + distance3
    distance = distance / 3
    return distance

GPIO.init()
GPIO_TRIGGER = port.PC7
GPIO_ECHO = port.PC4
GPIO.setcfg(GPIO_TRIGGER, GPIO.OUTPUT)
GPIO.setcfg(GPIO_ECHO, GPIO.INPUT)

GPIO.output(GPIO_TRIGGER, False)

if __name__ == "__main__":
  try:
   while True:

    distance = measure_average()
    print("Distance : %.1f" % distance)
    time.sleep(1)
  except KeyboardInterrupt:
   print("end")
