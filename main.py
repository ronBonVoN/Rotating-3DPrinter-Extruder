import dual_serial
import interpret_gcode

FILE_NAME = "CE3E3V2_print_test0_polygons.gcode"

def main(): 
    print("parsing gcode...")
    gcode = interpret_gcode.get_gcode(FILE_NAME)
    arduino_commands = interpret_gcode.arduino_commands(gcode)
    print("gcode parsing done, starting serial threads..")
    for line in arduino_commands:
        print(line)
    dual_serial.run_threads(gcode, arduino_commands)

if __name__ == "__main__":
    main()
