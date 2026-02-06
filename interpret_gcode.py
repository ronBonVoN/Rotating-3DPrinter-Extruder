import re
import math
import sys

EXTENSION_PRACTICAL_WIDTH = 8
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
        else:
            velocities.append(0)
    return velocities


def add_fillets(points, velocities, width, deg_tolerance):
    fillets = [[0,0] for _ in range(len(points))]

    for i in range(len(points) - 2):
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        if x1 == x2 and y1 == y2:
            continue

        for j in range(i+2, (len(points)-2)):
            x3, y3 = points[j]
            if x2 != x3 and y2 != y3:
                break

        length1 = math.hypot(x2 - x1, y2 - y1)
        length2 = math.hypot(x3 - x2, y3 - y2)
        if length1 <= width or length2 <= width:
            continue

        dot = (x2 - x1)*(x3 - x2) + (y2 - y1)*(y3 - y2)
        cross = (x2 - x1)*(y3 - y2) - (y2 - y1)*(x3 - x2)
        corner_angle = abs(math.atan2(cross, dot))
        if corner_angle < deg_tolerance or abs(corner_angle - math.pi) < deg_tolerance:
            continue

        start_dist = width / math.tan(corner_angle / 2)
        travel_before_fillet = length1 - start_dist 
        if velocities[i+1] <= 0:
            continue  
        time_before_fillet = travel_before_fillet/velocities[i+1]
        step_period = round(width/velocities[i+1]*1000)

        fillets[i+1] = [step_period, time_before_fillet]
    return fillets

def get_gcode(file_name): 
    gcode = read_gcode(file_name)
    edited_gcode = add_M400s(gcode)
    return edited_gcode

def arduino_commands(gcode):
    points = get_points(gcode)
    angles = get_angles(points)
    velocities = get_velocities(gcode)
    fillets = add_fillets(points, velocities, EXTENSION_PRACTICAL_WIDTH, DEG_TOLERANCE)
    arduino_commands = [[angles[i], fillets[i][0], fillets[i][1]] for i in range(len(gcode))]
    return arduino_commands








    
    




