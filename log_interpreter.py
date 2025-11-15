import matplotlib.pyplot as plt
import numpy as np
import re

file_name = "log_serial.txt"

try: 
    with open(file_name, "r") as f:
        lines = f.readlines()
except: 
    print(f"{file_name} not found")
    exit(1)

plt.ion()
fig, ax = plt.subplots()
ax.set_xlim(0, 250)
ax.set_ylim(0, 250)
ax.set_aspect('equal', adjustable='box')

x_data = []
y_data = []
rad_data = []
x0 = 0
y0 = 0
r = 30

line_plot, = ax.plot([], [], '-', color='blue')

for line in lines:

    if "X" in line and "Y" in line:
        input(line.strip())
        
        x_data.append(float(re.search(r"X(\d+\.?\d*)", line).group(1)))
        y_data.append(float(re.search(r"Y(\d+\.?\d*)", line).group(1)))

        x0, y0 = x_data[-1], y_data[-1]
        line_plot.set_data(x_data, y_data)

    if "angle: " in line:
        input(line.strip())
        
        rad_data.append(float(re.search(r"angle: (\d+\.?\d*)", line).group(1)))
        
        rad = rad_data[-1]
        x1 = x0 + r * np.cos(rad)
        y1 = y0 + r * np.sin(rad)
        ax.plot([x0, x1], [y0, y1], 'r-', linewidth=2)

    plt.draw()
    plt.pause(0.2)

print("program done")
plt.ioff()
plt.show()