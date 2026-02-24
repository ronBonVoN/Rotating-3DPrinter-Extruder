import matplotlib.pyplot as plt
import numpy as np
import re
import sys

FILE_NAME = "log_serial_polygons_for_debug.txt"

def read_file(file_name):
    try: 
        with open(file_name, "r") as f:
            lines = f.readlines()
    except: 
        print(f"{file_name} not found.")
        sys.exit(1)
    return lines

def active_plot(lines, start=0, end=0):
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_xlim(0, 250)
    ax.set_ylim(0, 250)
    ax.set_aspect('equal', adjustable='box')
    line_plot, = ax.plot([], [], '-', color='blue')

    x_data = [0]
    y_data = [0]
    r = 30
    
    if end <= start or end > len(lines):
        end = len(lines)

    for i in range(start, end): 
        if "X" in lines[i] and "Y" in lines[i]:
            x_match = re.search(r"X(\d+\.?\d*)", lines[i])
            y_match = re.search(r"Y(\d+\.?\d*)", lines[i])                  
            
            if x_match and y_match: 
                x = float(x_match.group(1))
                y = float(y_match.group(1))
                x_data.append(x)
                y_data.append(y)
                line_plot.set_data(x_data, y_data)
        
        elif "angle:" in lines[i]:
            rad_match = re.search(r"angle:([-+]?\d+\.?\d*)", lines[i])
            if rad_match:
                rad = float(rad_match.group(1))
                x = x_data[-1]
                y = y_data[-1] 
                ax.plot([x, x + r*np.cos(rad)], [y, y + r*np.sin(rad)], 'r-', linewidth=2)
        elif "A" in lines[i] and "P" in lines[i]: 
            pass
        else:
            continue

        command = input(f"{i}  " + lines[i].strip())
        if command == '\\': 
            ax.cla()
            ax.set_xlim(0, 250)
            ax.set_ylim(0, 250)
            ax.set_aspect('equal', adjustable='box')
            line_plot, = ax.plot([], [], '-', color='blue')
            x_data = [x_data[-1]]
            y_data = [y_data[-1]]
        
        plt.draw()
        plt.pause(0.2)

    print("program done")
    plt.ioff()
    plt.show()

def main():
    lines = read_file(FILE_NAME)
    active_plot(lines)

if __name__ == "__main__":
    main()