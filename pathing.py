import re
import math


file_name = "serial_example_prusa.gcode"
edited_gcode = []  
arduino_commands = []

start = False
width = 8


try: 
    with open(file_name, "r") as f:
        gcode = f.readlines()
except: 
    print(f"error finding {file_name}")
    exit(1)

for i in range(len(gcode)): 

    if start == False: 
        edited_gcode.append(gcode[i])
        arduino_commands.append(0)
        continue
    check_start(gcode[i]) # type: ignore
    
    x1, y1 = get_xy(gcode[i]) # type: ignore
    x2, y2 = get_xy(gcode[i+1]) # type: ignore
    x3, y3 = get_xy(gcode[i+2]) # type: ignore

    angle = get_angle(x1, y1, x2, y2) # type: ignore

    check_corner(x1, x2, x3, y1, y2, y3):  


def check_start(gcode_line): 
    if start == False:
        if re.search(rf"\b{"perimeter"}\b", gcode_line, re.IGNORECASE):
            start == True
            return
    else: 
        return

def get_xy(gcode_line):
    x_match = re.search(r'X(-?\d+\.?\d*)', gcode_line)
    y_match = re.search(r'Y(-?\d+\.?\d*)', gcode_line)

    x = float(x_match.group(1)) if x_match else None
    y = float(y_match.group(1)) if y_match else None

    return x, y

def get_angle(x1, y1, x2, y2): 
    if all(v is not None for v in (x1, y1, x2, y2)):
        angle = math.atan2(y2-y1, x2-x1)
        if (angle<0): 
            angle += 2*math.pi
        return angle
    else: 
        0.0

def check_corner(x1, x2, x3, y1, y2, y3):   
    if all(v is None for v in (x1, y1, x2, y2)):
        return None
    
    length1 = math.hypot(x2 - x1, y2 - y1)
    length2 = math.hypot(x3 - x2, y3 - y2)
    next_angle = get_angle(x2, y2, x3, y3)
    corner_angle = 180 - next_angle
    
    if corner_angle > 180: 
        return None
    
    fillet_radius = width*math.tan(corner_angle/2)
    start_dist = fillet_radius/math.tan(corner_angle/2)

    if length1 < start_dist or length2 < start_dist:
        return None
    
    return fillet_radius, start_dist

    

    
    


    

