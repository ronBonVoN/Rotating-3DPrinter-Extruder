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
cmd_info = queue.Queue(maxsize=1)

def format_arduino_command(arduino_commands, i): 
    return f"A{arduino_commands[i][0]} P{arduino_commands[i][1]}"

def send_gcode(ender, gcode):
    for i in range(len(gcode)):
        if gcode[i] == "" or gcode[i].startswith(";"):
            continue
        
        if "X" in gcode[i] and "Y" in gcode[i]:
            try:
                cmd_info.get_nowait()
            except queue.Empty:
                pass
            cmd_info.put((i, time.perf_counter()))

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

def send_arduino_commands(arduino, arduino_commands):
    while not stop_event.is_set():
        try:
            i, travel_start = cmd_info.get(timeout=0.1)
        except queue.Empty:
            continue

        if arduino_commands[i][2] > 0:
            travel_time = arduino_commands[i][2] - (time.perf_counter() - travel_start)
            if travel_time > 0:
                time.sleep(travel_time)

        command = format_arduino_command(arduino_commands, i)
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

def run_threads(gcode, arduino_commands):
    try:
        open(LOG_FILE_NAME, "w").close()
    except OSError:
        print(f"failed to create log file {LOG_FILE_NAME}")
        return

    try:
        arduino = serial.Serial(ARDUINO_COM, ARDUINO_BAUD, timeout=0.1)
        ender = serial.Serial(ENDER_COM, ENDER_BAUD, timeout=0.1)
    except serial.SerialException:
        print("failed to open serial ports.")
        return

    time.sleep(2)
    t1 = threading.Thread(target=send_gcode, args=(ender, gcode))
    t2 = threading.Thread(target=send_arduino_commands, args=(arduino, arduino_commands))
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
        log.put("forced close.\n")
        stop_event.set()

        t1.join()
        t2.join()
        t3.join()
    finally:
        print("closing serial connections...")
        arduino.close()
        ender.close()
        print("closed.")
