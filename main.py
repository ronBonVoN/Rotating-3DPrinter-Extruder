import dual_serial
import interpret_gcode

FILE_NAME = "CE3E3V2_D638-22.gcode"

def main(): 
    print("parsing gcode...")
    gcode = interpret_gcode.get_gcode(FILE_NAME)
    arduino_commands, wait_times = interpret_gcode.arduino_commands(gcode, print_output=True)
    print("gcode parsing done, starting serial threads..")
    dual_serial.run_threads(gcode, arduino_commands, wait_times)

if __name__ == "__main__":
    main()  
    