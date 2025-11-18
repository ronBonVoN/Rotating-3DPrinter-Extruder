import serial
import time

ARDUINO_COM = "COM12"
ENDER_COM = "COM14"
ARDUINO_BAUD = 115200
ENDER_BAUD = 115200

log_name = "log_serial.txt"
gcode_file_name = "air_square.gcode"
gocde = ""
motor = ""

arduino = serial.Serial(ARDUINO_COM, ARDUINO_BAUD, timeout=0.1)
ender = serial.Serial(ENDER_COM, ENDER_BAUD, timeout=0.1)

time.sleep(2)

try:
    with open(gcode_file_name, "r") as f:
        gcode = f.readlines().strip()
except FileNotFoundError:
    print(f"{gcode_file_name} not found")
    exit(1)

motor_gcode = gcode
for line in motor_gcode: 
    
        



with open(log_name, "a", encoding="ascii", errors="ignore") as log_file:
    try: 
        for i in range(len(lines)): 
            gcode = lines[i].strip()

            if gcode == "" or gcode.startswith(";"):
                continue
            
            ender.write((gcode + "\n").encode())
            print(gcode)
            log_file.write(gcode + "\n")  

            if "X" in gcode and "Y" in gcode: 
                for j in range(i+1, len(lines)): 
                    if "X" and "Y" in lines[j]: 
                        next_move = lines[j].strip()
                        arduino.write((next_move + "\n").encode())
            
            if arduino.in_waiting > 0:
                motor = arduino.readline().decode('utf-8', errors='ignore').strip()
                print(motor)
                log_file.write(motor + "\n")         

            while True:
                if ender.in_waiting > 0:
                    resp = ender.readline().decode('utf-8', errors='ignore').strip()
                    if "ok" in resp:
                        print("ok")
                        log_file.write("ok\n")
                        break
 
    except KeyboardInterrupt:
        print("forced close.")
        log_file.write("forced close.")

print("closing serial connections...")
arduino.close()
ender.close()
print("closed.")