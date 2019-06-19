import serial

ard = serial.Serial('/dev/ttyUSB0',9600,timeout=.1)
ard.flush()

while True :
    #ard.flushInput()
    data = ard.readline()[:-2]
    while(True): 
        g = input()
        if g == 1:
            ard.write(b'O')
        elif g == 0:
            ard.write(b'C')

  