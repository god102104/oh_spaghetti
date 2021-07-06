from socket import *
import subprocess
import os
import test as OD
#import OD_with_socket as OD
import asyncio
import threading
flag = False

async def tt():
 flag = False
 stop_thread = False
 past ="0\n"
 while True:
   ADDR = ('192.168.241.26',5050)
   clientSocket = socket(AF_INET, SOCK_STREAM)# 소켓을 생성한다.
   clientSocket.connect(ADDR)
   print("connect")
   data = clientSocket.recv(1024)
   data = data.decode()
   print(data)
   if past != data:
    OD.stop_thread = True
   if data=="1\n":
    print("Find")
    OD.ObjectDetection(clientSocket)
#    t = threading.Thread(target=OD.ObjectDetection, args = (clientSocket, stop_thread,))
 #   t.start()
   elif data == "2\n":
    os.system("rm ~/oh_spaghetti/result2.txt")
    popen = subprocess.Popen("python3 ~/oh_spaghetti/dog_bowl.py", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (stdoutdata, stderrdata) = popen.communicate()
    result = stdoutdata.decode().split(":")[1]
    print(stdoutdata.decode())
    print(result)
    print(len(result))
    if result == "full\n":
        clientSocket.send("Full".encode())
    else :
        clientSocket.send("Empty".encode())
    print("check")
   elif data == "3\n":
    print("aircon")
   past = data
 #  clientSocket.close()

if __name__ == "__main__":
    asyncio.run(tt())
