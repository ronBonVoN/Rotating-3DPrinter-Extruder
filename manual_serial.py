import serial
import time
## import re

com = "COM12"
baud_rate = 115200
file_name = "serial_example_prusa.gcode"
log_name = "log_serial.txt"

x1 = y1 = x2 = y2 = 0

try: 
    with open(file_name, "r") as f:
        lines = f.readlines()
except: 
    print(f"{file_name} not found")
    exit(1)

ser = serial.Serial(com, baud_rate, timeout=1)
time.sleep(2)

for line in lines: 

    if "G1" in line and "X" in line and "Y" in line: 
       ## x2 = float(re.search(r"X(\d+\.?\d*)", line).group(1))
       ## y2 = float(re.search(r"Y(\d+\.?\d*)", line).group(1))
       ## dist = ((x2-x1)**2+(y2-y1)**2)**0.5
       ## time.sleep(dist/30)
       ## x1 = x2
       ## y1 = y2
    
        try:
            response = ser.readline().decode(errors='ignore').strip()
            if response:
                input(response)
        except Exception as e:
            print("error reading serial:", e)
        
    # input(f"press enter to send: {line.strip()}")
        print(line.strip())
        ser.write((line.strip() + '\n').encode())
        time.sleep(0.1)

        with open(log_name, "w") as file:
            file.write(response + '\n')
            file.write(line.strip())

ser.close()
print("done!")






