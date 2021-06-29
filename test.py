#! /usr/bin/python
# -*- coding: utf-8 -*-

from socket import *
from select import *
import sys
from time import ctime

HOST = '192.168.219.108'
PORT = 5000
BUFSIZE = 1024
ADDR = (HOST,PORT)

clientSocket = socket(AF_INET, SOCK_STREAM)# 서버에 접속하기 위한 소켓을 생성한다.

try:
	clientSocket.connect(ADDR)# 서버에 접속을 시도한다.
	clientSocket.send('Hello!2'.encode())	# 서버에 메시지 전달

except  Exception as e:
    print('%s:%s'%ADDR)
    sys.exit()

print('connect is success')
