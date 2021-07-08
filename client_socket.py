from socket import *
import subprocess
import os
import findDog as FD
import dog_bowl as bowl
import user_setting as usr
from gpiozero import LED
from time import sleep

flag = False
_led = LED(17)

while True:
   clientSocket = socket(AF_INET, SOCK_STREAM) 
   ADDR = (usr.Mobile,5050)
   clientSocket.connect(ADDR)
   print("connect") #socket connection check
   _led.off()
   if not flag :
    data = clientSocket.recv(1024)
    data = data.decode()
   print(data)
   if data=="1\n":
    flag = True
    print("Find!!") #dog-Object find message
    past = data
    data = FD.findDog(clientSocket)
   elif data == "2\n":
    flag = True
    print("Check!!") #dog-food check message
    result = bowl.remain_food_check()
    if not result:
        result = "Full" #result (Full, Empty)
    if result:
        print(result)
        clientSocket.send(result.encode())
    flag = False 
   elif data == "3\n":
    flag = True
    _led.on()
 
    print("Aircon!!") 
    flag = False
   clientSocket.close()
