import serial
import time

ArduinoSerial = serial.Serial('com4', 9600)
time.sleep(2)
print(ArduinoSerial.readline())
while 1:
    var = input("press 1 or 0 or 2\n")
    print("you entered: ", var)

    if var == '0':
        ArduinoSerial.write(b'0')
    if var == '1':
        ArduinoSerial.write(b'1')
    if var == '2':
        ArduinoSerial.write(b'2')
