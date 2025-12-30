import re
import math
import turtle

file_name = "Shape-Box_51m_0.24mm_205C_PLA_ENDER3S1PLUS.gcode"
nozel_path = []

start = False
wipe = False
layer_change = False
width = 8

t = turtle.Turtle()
screen = turtle.Screen()
screen.setup(250, 250)
screen.setworldcoordinates(0, 0, 250, 250)

def check_start(gcode_line, start): 
    if not start:
        if re.search(r"\bperimeter\b", gcode_line, re.IGNORECASE):
            return True
    return start
    
def check_wipe(gcode_line, wipe): 
    if not wipe and ";WIPE_START" in gcode_line:
        return True
    if wipe and ";TYPE:" in gcode_line:
        return False
    return wipe
    
def check_layer_change(gcode_line, layer_change):
    if not layer_change and ";LAYER_CHANGE" in gcode_line:
        return True
    if layer_change and ";TYPE:" in gcode_line:
        return False 
    return layer_change

def get_xy(gcode_line):
    if ";" in gcode_line:
        return -1, -1
    
    x_match = re.search(r'X(-?\d+\.?\d*)', gcode_line)
    y_match = re.search(r'Y(-?\d+\.?\d*)', gcode_line)

    x = float(x_match.group(1)) if x_match else -1
    y = float(y_match.group(1)) if y_match else -1

    return x, y

def alternate_layers(nozel_path, gcode): 
    sections = []
    start = None
    end = None
    for i in range(len(nozel_path)): 
        if nozel_path[i] == -2 and nozel_path[i+1] != -2: 
            start = i 
        if nozel_path[i] != -2 and nozel_path[i+1] == -2:
            end = i
        if start != None and end != None: 
            sections.append((start, end))
            start = None
            end = None
    
    
def fillet_corners(nozel_path, gcode):   
    for i in range(len(nozel_path) - 2):
        x1, y1 = nozel_path[i]
        x2, y2 = nozel_path[i+1]
        x3, y3 = nozel_path[i+2]
        
        if all(v > -1 for v in (x1, y1, x2, y2, x3, y3)):
            length1 = math.hypot(x2 - x1, y2 - y1)
            length2 = math.hypot(x3 - x2, y3 - y2)
            
            dot = (x1-x2)*(x3-x2) + (y1-y2)*(y3-y2)
            cos_theta = dot / (length1 * length2)
            cos_theta = max(-1.0, min(1.0, cos_theta))
            corner_angle = math.acos(dot/(cos_theta))
            
            fillet_radius = width*math.tan(corner_angle/2)
            start_dist = fillet_radius/math.tan(corner_angle/2)

            if length1 < start_dist or length2 < start_dist:
                continue
            
            cmd = f"; ARDUINO_FILLET L{length1} D{start_dist} R{fillet_radius} A{corner_angle}\n"
            gcode[i+1] = gcode[i+1].replace("\n", cmd)

try: 
    with open(file_name, "r") as f:
        gcode = f.readlines()
except: 
    print(f"error finding {file_name}")
    exit(1)

for gcode_line in gcode: 
    start = check_start(gcode_line, start) 
    if not start: 
        nozel_path.append((-1,-1))
        continue

    layer_change = check_layer_change(gcode_line, layer_change)
    if layer_change:
        nozel_path.append((-2,-2))
        continue   
    
    wipe = check_wipe(gcode_line, wipe) 
    if wipe:
        nozel_path.append((-1,-1))
        continue
    
    x, y = get_xy(gcode_line) 
    nozel_path.append((x,y))

for x, y in nozel_path: 
    print(f"{x}, {y}")

#  t.penup()
#  for x, y in nozel_path: 
#      if x > -1 and y > -1: 
#          t.goto(x,y)
#         t.pendown()
#         break
# for x, y in nozel_path: 
#     if x > -1 and y > -1: 
#         t.goto(x,y)

# turtle.done()



    

    
    


    

