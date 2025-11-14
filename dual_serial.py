import serial
import time

ARDUINO_COM = "COM12"
ENDER_COM = "COM13"
ARDUINO_BAUD = 115200
ENDER_BAUD = 115200

log_name = "log_serial.txt"
motor = ""
gcode = ""

arduino = serial.Serial(ARDUINO_COM, ARDUINO_BAUD, timeout=0.1)
ender = serial.Serial(ENDER_COM, ENDER_BAUD, timeout=0.1)

time.sleep(2)

try: 
    
    while True: 

        if ender.in_waiting>0:
            
            gcode = ender.readline().decode('utf-8', errors='ignore').strip()
            
            if not gcode.startswith("echo:busy"):
                arduino.write((gcode + '\n').encode('utf-8'))
                print(gcode)
                if arduino.in_waiting > 0: 
                    motor = arduino.readline().decode('utf-8', errors='ignore').strip()
                    print(motor)
            
            if motor or gcode: 
                with open(log_name, "a", encoding="ascii", errors="ignore") as file:
                    if motor:
                        file.write(motor + '\n')
                    if gcode:
                        file.write(gcode + '\n')

        time.sleep(0.01)

except KeyboardInterrupt: 
    print("closing serial connections...")
    arduino.close()
    ender.close()
    print("closed.")






