# import serialser = serial.Serial('COM3')  # open serial port

# data = []
# size = ser.inWaiting()
# data.append(ser.read(size))
# print(data)
# # check which port was really used
# ser.write(b'hello')     # write a string
# ser.close()             # close port


import serial
import time
z1baudrate = 9600
z1port = 'COM10'  # set the correct port before run it

z1serial = serial.Serial(port=z1port, baudrate=z1baudrate)
z1serial.timeout = 2  # set read timeout
# print z1serial  # debug serial.
print(z1serial.is_open)  # True for opened
if z1serial.is_open:
    while True:
        size = z1serial.inWaiting()
        if size:
            data = z1serial.read(size)
            arr= list(data.splitlines())
            for i in range(len(arr)):
                print(arr[i]);

        time.sleep(1)
else:
     print('z1serial not open')


