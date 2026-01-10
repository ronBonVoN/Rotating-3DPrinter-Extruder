import re
import math
import sys

FILE_NAME = "CE3E3V2_triangle.gcode"
WIDTH = 8 # mm 
DEG_TOLERANCE = math.radians(2)

def read_file(file_name):
    try: 
        with open(file_name, "r") as f:
            gcode = f.readlines()
            return gcode
    except: 
        print(f"error finding {file_name}")
        exit(1)

def get_xy(gcode_line):
    if ";" in gcode_line:
        return None, None
    
    x_match = re.search(r'X(-?\d+\.?\d*)', gcode_line)
    y_match = re.search(r'Y(-?\d+\.?\d*)', gcode_line)

    if x_match and y_match: 
        x = float(x_match.group(1)) 
        y = float(y_match.group(1))
        return x, y 
    else:
        return None, None
    
def fillet_corners(gcode, width, deg_tolerance):   
    edited_gcode = gcode.copy()
    
    point_idx = []
    points = []
    lines_to_read = len(gcode)
    for i in range(len(gcode)): 
        x, y = get_xy(gcode[i])
        if None not in (x, y): 
            point_idx.append(i)
            points.append((x, y))
        sys.stdout.write(f"\r{i+1} out of {lines_to_read} lines to read...")
        sys.stdout.flush()
    
    points_to_read = len(points) - 2
    for p in range(points_to_read):
        x1, y1 = points[p]
        x2, y2 = points[p+1]
        x3, y3 = points[p+2]
            
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
        cmd = f" ;L{length1:.3f} A{corner_angle:.3f} D{start_dist}\n FILLET"
        edited_gcode[point_idx[p+1]] = edited_gcode[point_idx[p+1]].replace("\n", cmd)

        sys.stdout.write(f"\r{p+1} out of {points_to_read} points to analyze...")
        sys.stdout.flush()
    
    return edited_gcode

def create_new_file(file_name, edited_gcode): 
    new_file_name = file_name.replace(".gcode", " edited.gcode")
    with open(new_file_name, "w") as f:
        f.writelines(edited_gcode)

def main(): 
    gcode = read_file(FILE_NAME)
    edited_gcode = fillet_corners(gcode, 8, DEG_TOLERANCE)
    create_new_file(FILE_NAME, edited_gcode)

if __name__ == "__main__":
    main()
    

    
    


    

