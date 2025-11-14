; --- Simple Ender 3 slow motion test (no heat, no extrusion, with accurate XY position reporting) ---
G90
G21
G28

G1 Z40 F300
M400                ; wait for move to complete
M114                ; now report position

; move to start position (bottom-left corner offset 25 mm in X and Y)
G1 X25 Y25 F600

; draw 40x40 mm square in the air
G1 X65 Y25 F600
M400
M114
G1 X65 Y65 F600
M400
M114
G1 X25 Y65 F600
M400
M114
G1 X25 Y25 F600
M400
M114

; optional: lower a bit and disable motors
G1 Z10 F300
M400
M84

; --- end of motion test ---
