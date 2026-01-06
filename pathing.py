import re
import math
import sys

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

def fillet_corners(gcode, width):   
    lines_to_read = len(gcode)
    edited_gcode = gcode
    
    for i in range(lines_to_read):
        
        x1, y1 = get_xy(gcode[i])
        if None in (x1, y1): 
            continue
        
        for j in range(i + 1, lines_to_read):
            x2, y2 = get_xy(gcode[j])
            if x2 != None and y2 != None:
                break
        
        for k in range(j + 1, lines_to_read):
            x3, y3 = get_xy(gcode[k])
            if x3 != None and y3 != None: 
                break
        
        if k + 1 == lines_to_read: 
            break
            
        length1 = math.hypot(x2 - x1, y2 - y1)
        length2 = math.hypot(x3 - x2, y3 - y2)

        eps = 1e-9
        if length1 <= eps or length2 <= eps:
            continue

        ux, uy = x1 - x2, y1 - y2
        vx, vy = x3 - x2, y3 - y2

        dot = ux*vx + uy*vy
        cross = ux*vy - uy*vx

        corner_angle = abs(math.atan2(cross, dot))

        if corner_angle <= eps:
            continue

        min_angle = math.radians(1)  
        if corner_angle < min_angle:
            continue

        start_dist = width / math.tan(corner_angle / 2)

        if length1 <= start_dist or length2 <= start_dist:
            continue
        
        cmd = f" ;FILLET L{length1:.3f} L'{length2:.3f} D{start_dist:.3f} R{width:.3f} A{corner_angle:.3f}\n"
        edited_gcode[i] = edited_gcode[i].replace("\n", cmd)

        sys.stdout.write(f"\r{i+1} out of {lines_to_read} lines read...")
        sys.stdout.flush()
    
    return edited_gcode

def create_new_file(file_name, edited_gcode): 
    new_file_name = file_name.replace(".gcode", " edited.gcode")
    with open(new_file_name, "w") as f:
        f.writelines(edited_gcode)

file_name = "CE3E3V2_flat block.gcode"
gcode = read_file(file_name)
edited_gcode = fillet_corners(gcode, 8)
create_new_file(file_name, edited_gcode)



    

    
    


    

