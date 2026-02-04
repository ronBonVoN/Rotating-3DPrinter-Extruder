import matplotlib.pyplot as plt
import numpy as np
import math
import re

def read_file(file_name):
    try: 
        with open(file_name, "r") as f:
            lines = f.readlines()
    except: 
        print(f"{file_name} not found")
        exit(1)
    return lines

    
def active_plot(lines):
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_xlim(0, 250)
    ax.set_ylim(0, 250)
    ax.set_aspect('equal', adjustable='box')

    x_data = [0]
    y_data = [0]
    rad_data = []
    r = 30

    line_plot, = ax.plot([], [], '-', color='blue')

    for i in range(len(lines)): 
        X_match = re.search(r"X(\d+\.?\d*)", lines[i])
        Y_match = re.search(r"Y(\d+\.?\d*)", lines[i])
        T_match = re.search(r"T(\d+\.?\d*)", lines[i])
        angle_match = re.search(r"angle: (\d+\.?\d*)", lines[i])

        if X_match and Y_match:
            x = float(X_match.group(1))
            y = float(Y_match.group(1))
        
            if T_match: 
                fillet_dist = float(T_match.group(1))
                angle = math.atan2(y - y_data[-1], x - x_data[-1])  
                x_data.append(x_data[-1] + fillet_dist*math.cos(angle))
                y_data.append(y_data[-1] + fillet_dist*math.sin(angle))

            x_data.append(x)
            y_data.append(y)
            line_plot.set_data(x_data, y_data)

        elif angle_match:
            rad = float(angle_match.group(1))  
            rad_data.append(rad)

            if "CORNER" in lines[i] and "FILLET" in lines[i+1]:
                x = x_data[-2]
                y = y_data[-2]
            else: 
                x = x_data[-1]
                y = y_data[-1] 

            ax.plot([x, x + r*np.cos(rad)], [y, y + r*np.sin(rad)], 'r-', linewidth=2)
        else:
            continue

        input(lines[i].strip())
        plt.draw()
        plt.pause(0.2)

    print("program done")
    plt.ioff()
    plt.show()

def main():
    file_name = "log_serial.txt"
    lines = read_file(file_name)
    active_plot(lines)


if __name__ == "__main__":
    main()