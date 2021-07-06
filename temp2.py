import os
from socket import *

flag = False
while True:
  if flag == False:
    flag = True
    cs = socket(AF_INET, SOCK_STREAM)#
    cs.connect(('172.30.1.50',5050))
    cs.send("find".encode())
    cs.close()
