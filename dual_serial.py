import serial
import time
import threading
import queue

ARDUINO_COM = "COM14"
ENDER_COM = "COM13"
ARDUINO_BAUD = 115200
ENDER_BAUD = 115200

gcode_file_name = "air_square_2x edited.gcode"
log_file = "log_serial.txt"

arduino = serial.Serial(ARDUINO_COM, ARDUINO_BAUD, timeout=0.1)
ender = serial.Serial(ENDER_COM, ENDER_BAUD, timeout=0.1)

time.sleep(2)

try:
    with open(gcode_file_name, "r") as f:
        gcode = [line.strip() for line in f.readlines()]
except FileNotFoundError:
    print(f"{gcode_file_name} not found")
    exit(1)

stop_event = threading.Event()
log_queue = queue.Queue()

def send_gcode():
    for command in gcode:     
        if command == "" or command.startswith(";"):
            continue
        
        ender.write((command + "\n").encode())
        arduino.write((command + "\n").encode())
        
        print(command)
        log_queue.put(command + "\n")
       # stop_event.wait(3)
       # print("ok")
        log_queue.put("ok\n")
        while not stop_event.is_set():
            if ender.in_waiting > 0:
                if "ok" in ender.readline().decode('utf-8', errors='ignore').strip():
                    print("ok")
                    log_queue.put("ok\n")
                    break
            time.sleep(0.01)

    stop_event.set()


def read_arduino():
    while not stop_event.is_set():
        if arduino.in_waiting > 0:
            motor = arduino.readline().decode('utf-8', errors='ignore').strip()
            print(motor)
            log_queue.put(motor + "\n")  
        time.sleep(0.01)

def write_to_log():
    with open(log_file, "a") as f:
        while not stop_event.is_set() or not log_queue.empty():
            try:
                f.write(log_queue.get(timeout=0.1))
                f.flush()   # ensures real-time writing
            except queue.Empty:
                pass


t1 = threading.Thread(target=send_gcode)
t2 = threading.Thread(target=read_arduino)
t3 = threading.Thread(target=write_to_log)

try:
    t1.start()
    t2.start()
    t3.start()
  
    t1.join()
    t2.join()
    t3.join()
except KeyboardInterrupt:
    print("forced close...")
    log_queue.put("forced close.\n")
    stop_event.set()
    
    t1.join()
    t2.join()
    t3.join()

print("closing serial connections...")
arduino.close()
ender.close()
print("closed.")