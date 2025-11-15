import serial
import time

ARDUINO_COM = "COM12"
ENDER_COM = "COM13"
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
        lines = f.readlines()
except FileNotFoundError:
    print(f"{gcode_file_name} not found")
    exit(1)

with open(log_name, "a", encoding="ascii", errors="ignore") as log_file:
    try:
        for line in lines:
            gcode = line.strip()

            if gcode == "" or gcode.startswith(";"):
                continue

            ender.write((gcode + "\n").encode())
            print(gcode)
            log_file.write(gcode + "\n")
            
            while True:
                if ender.in_waiting > 0:
                    resp = ender.readline().decode('utf-8', errors='ignore').strip()
                    if "ok" in resp:
                        print("ok")
                        log_file.write("ok")
                        break

            arduino.write((gcode + "\n").encode())
            if arduino.in_waiting > 0:
                motor = arduino.readline().decode('utf-8', errors='ignore').strip()
                print(motor)
                log_file.write(motor + "\n")
 
    except KeyboardInterrupt:
        print("closing serial connections...")
        arduino.close()
        ender.close()
        print("closed.")
