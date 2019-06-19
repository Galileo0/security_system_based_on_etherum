
import cv2
import numpy as np
import pytesseract
from PIL import Image
from pytesseract import image_to_string
import socket
from threading import *

def test2():
    cap = cv2.VideoCapture(0)
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        ret,frame = cap.read()
        cv2.imshow('Current',frame)
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        image = Image.fromarray(gray)
        
        data = pytesseract.image_to_string(image)
        




def test():
    cap = cv2.VideoCapture(0)
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        ret, frame = cap.read()
        cv2.imshow('Current',frame)
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        image = Image.fromarray(gray)
        data = pytesseract.image_to_string(image)
        print (data)

test()
'''
card_sources = "images/"
card_input =  raw_input("Enter Your Card [Name of pic now]-> ")
card = card_sources + card_input 
data = pytesseract.image_to_string(Image.open(card))
#handel string
data = data.replace('\n\n', '\n')


print data

#send Data over Tcp

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    security_B_ip = '192.168.1.4'
    security_B_port = 8000
    s.connect((security_B_ip,security_B_port))
    s.send(data.encode())
    #s.recv(1024)
    #input()
except socket.error:
    print('Failed to create socket')
    

'''
