from socket import *
import findDog as FD
import dog_bowl as bowl
import user_setting as usr
from gpiozero import LED
from time import sleep

flag = False
_led = LED(17)

while True:
   #안드로이드 앱과 통신
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
    print("Find!!") 
    past = data
    #Find 명령 수행
    data = FD.findDog(clientSocket)
   elif data == "2\n":
    flag = True
    print("Check!!") 
    #먹이확인 명령 수행
    result = bowl.remain_food_check()
    if not result: # 판별 실패 시 에러를 방지하기 위해 사용
        result = "Full" 
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
