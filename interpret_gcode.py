import re
import math
import sys

EXTENSION_PRACTICAL_WIDTH = 10
DEG_TOLERANCE = math.radians(2)

def read_gcode(file_name):
    try:
        with open(file_name, "r") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
            print(f"{file_name} not found.")
            sys.exit(1)   
     
def add_M400s(gcode): 
    edited_gcode = []
    for line in gcode:
        edited_gcode.append(line)
        if line.strip().startswith(("G0", "G1")):
            edited_gcode.append("M400")
    return edited_gcode

def get_points(gcode): 
    points = []
    for line in gcode:         
        x_match = re.search(r'X(-?\d+\.?\d*)', line)
        y_match = re.search(r'Y(-?\d+\.?\d*)', line)

        if x_match and y_match: 
            points.append((float(x_match.group(1)), float(y_match.group(1))))
        elif len(points) == 0:
            points.append((0,0))
        else:
            points.append(points[-1])
    return points
        
def get_angles(points): 
    angles = [0.0]
    for i in range(1, len(points)):        
        x1, y1 = points[i-1]
        x2, y2 = points[i]
        dx = x2 - x1
        dy = y2 - y1

        if dx == 0 and dy == 0:
            angles.append(angles[-1])
        else:
            angles.append(round(math.atan2(dy, dx),4))
    return angles 

def get_velocities(gcode):
    velocities = []
    for line in gcode:
        f_match = re.search(r'F(-?\d+\.?\d*)', line)
        if f_match:
            velocities.append(float(f_match.group(1))/60)
        elif len(velocities) == 0 or velocities[-1] == 0:
            velocities.append(0)
        else:
            velocities.append(velocities[-1])
    return velocities

def get_fillets(gcode, points, angles, velocities, width, deg_tolerance):
    step_periods = [0 for _ in range(len(points))]
    wait_times = [0 for _ in range(len(points))]

    for i in range(len(points) - 2):
        if "G1" not in gcode[i+1]:
            continue
        
        if velocities[i] <= 0:
            continue  
        
        angle1 = angles[i]
        angle2 = angles[i+1]
        if angles[i] == angles[i+1]:
            continue
      
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        length = math.hypot(x2 - x1, y2 - y1)
        if length <= width:
            continue
        
        corner_angle = abs(math.atan2(math.sin(angle2 - angle1), math.cos(angle2 - angle1)))
        if corner_angle < deg_tolerance or abs(corner_angle - math.pi) < deg_tolerance:
            continue

        wait_times[i] = round((length - width)/velocities[i],4)
        step_periods[i+1] = round(width/velocities[i]*1000/2)
        
    return step_periods, wait_times

def get_gcode(file_name): 
    gcode = read_gcode(file_name)
    edited_gcode = add_M400s(gcode)
    return edited_gcode

def arduino_commands(gcode, print_output=False):
    points = get_points(gcode)
    angles = get_angles(points)
    velocities = get_velocities(gcode)
    step_periods, wait_times = get_fillets(gcode, points, angles, velocities, EXTENSION_PRACTICAL_WIDTH, DEG_TOLERANCE)
    arduino_commands = [f"A{angles[i]} P{step_periods[i]} W{wait_times[i]}" for i in range(len(gcode))]
    if (print_output):
        [print(f"{arduino_commands[i]}") for i in range(len(gcode))]
    return arduino_commands, wait_times








    
    




