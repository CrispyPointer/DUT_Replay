from socket import timeout
from turtle import delay
import serial
import time
from datetime import timedelta
import serial as ser

# ser = serial.Serial()
# port = input("Enter Serial port: ")
# ser = serial.Serial(
#     port = port,
#     baudrate = 115200,
#     parity=serial.PARITY_NONE,
#     stopbits=serial.STOPBITS_ONE,
#     bytesize=serial.EIGHTBITS,
#     timeout = 1
# )
# ser.setDTR(False)
# ser.setRTS(False)
# print("Start reading in 2 seconds...")
# time.sleep(2)
# ser.isOpen()

# Create datetime string
time_str = "[23:02:11:430]"
def time_extract(time_str):
    hour = int(time_str[1:3])
    minute = int(time_str[4:6])
    second = int(time_str[7:9])
    millisecond = int(time_str[10:13])
    current_time = timedelta(hours= hour, minutes= minute, seconds= second, microseconds= millisecond*1000)
    return current_time

#Quick calculating two timestamps 
timeA = timedelta(hours=0, minutes=6, seconds=59, milliseconds=478)
timeB = timedelta(hours=0, minutes=7, seconds=1, milliseconds= 468)

timeC = timeB - timeA
#print(timeC.microseconds)

with open('LOG00258.txt') as f:
    previous_time = timedelta()
    current_time =  timedelta()
    for line in f.readlines():
        if (line[0] == '[' and line[13] == ']'):
            
            #Read first line with timestamp
            if(current_time.seconds == 0):
                print(line)
                current_time =  time_extract(line)
                continue
            previous_time = current_time
            #print(previous_time)
            current_time =  time_extract(line)
            #print(current_time)

            #If the device traveled back time :)
            if(current_time < previous_time):
                print(line)
                previous_time = time_extract(line)
                continue
            delay_time = current_time - previous_time
            #ser.write(line.encode())
            duration = delay_time.seconds + (delay_time.microseconds/1000000)
            #print(duration)
            time.sleep(duration)
            print(line)
        else:
            print(line)



