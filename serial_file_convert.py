import os 

input_filename = "serial_example.txt"
output_filename = "serial_example.cpp"

try: 
    with open(input_filename, "r") as fin:
        print(os.getcwd())
        lines = fin.readlines()
        print(fin.readlines())
except: 
    print("0")
    exit(1)

with open(output_filename, "w") as fout: 
    fout.write("#include <Arduino.h>\n\n")
    fout.write("const char serial_example[] PROGMEM =\n")

    for line in lines: 
        line = line.rstrip("\n")
        escaped_line = line.replace('"', '\\"')
        fout.write(f'"{escaped_line}\\n"\n')

    fout.write(";\n")
    print("1")
    