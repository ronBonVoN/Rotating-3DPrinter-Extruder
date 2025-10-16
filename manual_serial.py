import serial
import time

com = "COM12"
baud_rate = 9600
file_name = "serial_example.txt"

try: 
    with open(file_name, "r") as f:
        lines = f.readlines()
except: 
    print(f"{file_name} not found")
    exit(1)

ser = serial.Serial(com, baud_rate, timeout=1)
time.sleep(2)

for line in lines: 
    input(f"press enter to send: {line.strip()}")
    ser.write((line.strip() + '\n').encode())
    time.sleep(0.1)

ser.close()
print("done!")





