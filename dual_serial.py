import serial
import time
import threading
import queue

ARDUINO_COM = "COM14"
ENDER_COM = "COM15"
ARDUINO_BAUD = 115200
ENDER_BAUD = 115200
LOG_FILE_NAME = "log_serial.txt"

stop_event = threading.Event()
log = queue.Queue()
wait_index = queue.Queue(maxsize=1)
arduino_index = queue.Queue(maxsize=1)

def send_gcode(ender, gcode):
    for i in range(len(gcode)):
        if gcode[i] == "" or gcode[i].startswith(";"):
            continue
        
        try:
            wait_index.get_nowait()
        except queue.Empty:
            pass
        wait_index.put(i)

        ender.write((gcode[i] + "\n").encode())
        log.put(gcode[i])

        while not stop_event.is_set():
            if ender.in_waiting > 0:
                response = ender.readline().decode("utf-8", errors="ignore").strip()
                if "ok" in response:
                    log.put("ok")
                    break
            time.sleep(0.01)
    stop_event.set()

def arduino_wait(wait_times, gcode):
    while not stop_event.is_set():
        try:
            i = wait_index.get(timeout=0.01)
        except queue.Empty:
            continue 
        
        if "G1" in gcode[i] and "X" in gcode[i] and "Y" in gcode[i]:
            try:
                arduino_index.get_nowait()
            except queue.Empty:
                pass
            arduino_index.put(i)

        if len(gcode) < i+1: 
            continue
        
        wait_time = wait_times[i+1] 
        if wait_time <= 0: 
            continue
        
        if "G1" not in gcode[i+1] or "X" not in gcode[i+1] or "Y" not in gcode[i+1]:
            continue
        
        start = time.perf_counter()
        while not stop_event.is_set():
            if time.perf_counter() - start >= wait_time: 
                try:
                    arduino_index.get_nowait()
                except queue.Empty:
                    pass
                arduino_index.put(i+1)
                break
            try:
                i = wait_index.get(timeout=0.01)
            except queue.Empty:
                continue
            if "G1" in gcode[i] and "X" in gcode[i] and "Y" in gcode[i]:
                wait_index.put(i)
                break

def send_arduino_commands(arduino, arduino_commands):
    while not stop_event.is_set():
        try:
            i = arduino_index.get(timeout=0.01)
        except queue.Empty:
            continue

        command = arduino_commands[i]
        arduino.write((command + "\n").encode())
        log.put(command)

        while not stop_event.is_set():
            if arduino.in_waiting > 0:
                response = arduino.readline().decode("utf-8", errors="ignore").strip()
                log.put(response)
                break
            time.sleep(0.01)        

def write_to_log():
    with open(LOG_FILE_NAME, "a") as f:
        while True:
            if stop_event.is_set() and log.empty():
                break
            try:
                message = log.get(timeout=0.1)
                print(message)
                f.write(message + "\n")
                f.flush()
            except queue.Empty:
                continue

def run_threads(gcode, arduino_commands, wait_times):
    try:
        open(LOG_FILE_NAME, "w").close()
    except OSError as e:
        print(f"failed to create log file {LOG_FILE_NAME}: {e}")
        return

    try:
        arduino = serial.Serial(ARDUINO_COM, ARDUINO_BAUD, timeout=0.1)
        ender = serial.Serial(ENDER_COM, ENDER_BAUD, timeout=0.1)
    except serial.SerialException as e:
        print(f"failed to open serial ports: {e}")
        return
    time.sleep(2)

    t1 = threading.Thread(target=arduino_wait, args=(wait_times, gcode,))
    t2 = threading.Thread(target=send_gcode, args=(ender, gcode,))
    t3 = threading.Thread(target=send_arduino_commands, args=(arduino, arduino_commands,))
    t4 = threading.Thread(target=write_to_log)

    try:
        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
    except KeyboardInterrupt:
        log.put("forced close.\n")
        stop_event.set()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
    finally:
        print("closing serial connections...")
        arduino.close()
        ender.close()
        print("closed.")
