from socket import *
import subprocess
import os
import findDog as FD
import dog_bowl as bowl
import user_setting as usr
flag = False


while True:
   clientSocket = socket(AF_INET, SOCK_STREAM)
   ADDR = (usr.Mobile,5050)
   clientSocket.connect(ADDR)
   print("connect")
   if not flag :
    data = clientSocket.recv(1024)
    data = data.decode()
   print(data)
   if data=="1\n":
    flag = True
    print("Find!!")
    past = data
    data = FD.findDog(clientSocket)
   elif data == "2\n":
    flag = True
    print("Check!!")
    result = bowl.remain_food_check()
    if not result:
        result = "Full"
    if result:
        print(result)
        clientSocket.send(result.encode())
    flag = False 
   elif data == "3\n":
    flag = True
    
    print("Aircon!!")
    flag = False
   clientSocket.close()
