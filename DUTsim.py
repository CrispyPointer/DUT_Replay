from socket import timeout
#from turtle import delay
import serial
import time
from datetime import timedelta
import serial as ser


#Set up serial port (COM# on Windows, /dev/ttyUSB# on Linux)
ser = serial.Serial()
port = input("Enter Serial port: ")
ser = serial.Serial(
    port = port,
    baudrate = 115200, #Standard 115200 8N1 UART setup
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout = 1
)
ser.setDTR(False)
ser.setRTS(False)
print("Start sending in 2 seconds...")
time.sleep(2)
ser.isOpen()

# Create datetime string (just to test with different timestamps)
time_str = "[23:02:11:430]"
def time_extract(time_str):
    hour = int(time_str[1:3])
    minute = int(time_str[4:6])
    second = int(time_str[7:9])
    millisecond = int(time_str[10:13])
    current_time = timedelta(hours= hour, minutes= minute, seconds= second, microseconds= millisecond*1000)
    return current_time

#Quickly calculate two timestamps (Test)
timeA = timedelta(hours=0, minutes=6, seconds=59, milliseconds=478)
timeB = timedelta(hours=0, minutes=7, seconds=1, milliseconds= 468)
timeC = timeB - timeA
#print(timeC.microseconds)

#Start Replaying !!
with open('LOG00001.TXT', mode= 'r', encoding='ISO_8859_1') as f:
    previous_time = timedelta()
    current_time =  timedelta()

    for line in f.readlines():
        if (line[0] == '[' and line[13] == ']'):
            
            #Read first line with timestamp
            if(current_time.seconds == 0):
                print(line)
                ser.write(line.encode())
                current_time =  time_extract(line)
                continue
            previous_time = current_time  

            #print(previous_time)
            current_time =  time_extract(line)
            #print(current_time)

            #If the device traveled to the future :)
            if(current_time < previous_time):
                print(line)
                ser.write(line.encode())
                previous_time = time_extract(line)
                continue
            delay_time = current_time - previous_time   #Calculate the delay duration (In timestamp datatype)
            duration = delay_time.seconds + (delay_time.microseconds/1000000)   #So it will delay accurately in milliseconds
            #print(duration)
            time.sleep(duration)
            print(line)
            ser.write(line.encode())
        else:
            print(line)
            ser.write(line.encode())

ser.close() #Nicely close the serial port

