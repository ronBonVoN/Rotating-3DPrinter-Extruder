;FLAVOR:Marlin
;TIME:73
;Filament used: 0.046634m
;Layer height: 0.2
;MINX:77.3
;MINY:77.3
;MINZ:0.2
;MAXX:157.7
;MAXY:157.7
;MAXZ:0.2
;Generated with Cura_SteamEngine 5.2.1
M140 S65
M105
M190 S65
M104 S205
M105
M109 S205
M82 ;absolute extrusion mode
; Ender 3 Custom Start G-code
G92 E0 ; Reset Extruder
G28 ; Home all axes
G1 Z2.0 F3000 ; Move Z Axis up little to prevent scratching of Heat Bed
M400
G1 X0.1 Y20 Z0.3 F5000.0 ; Move to start position
M400
G1 X0.1 Y200.0 Z0.3 F1500.0 E15 ; Draw the first line
M400
G1 X0.4 Y200.0 Z0.3 F5000.0 ; Move to side a little
M400
G1 X0.4 Y20 Z0.3 F1500.0 E30 ; Draw the second line
M400
G92 E0 ; Reset Extruder
G1 Z2.0 F3000 ; Move Z Axis up little to prevent scratching of Heat Bed
M400
G1 X5 Y20 Z0.3 F5000.0 ; Move over to prevent blob squish
M400
G92 E0
G92 E0
;LAYER_COUNT:1
;LAYER:0
M107
G0 F6000 X77.7 Y157.3 Z0.2
M400
;TYPE:WALL-OUTER
G1 F1200 X157.3 Y157.3 E2.64751
M400
G1 X157.3 Y77.7 E5.29501
M400
G1 X77.7 Y77.7 E7.94252
M400
G1 X77.7 Y157.3 E10.59003
M400
G0 F6000 X77.3 Y157.7
M400
G1 F1200 X77.3 Y77.3 E13.26414
M400
G1 X157.7 Y77.3 E15.93826
M400
G1 X157.7 Y157.7 E18.61237
M400
G1 X77.3 Y157.7 E21.28649
M400
G0 F6000 X98.621 Y150.2
M400
G1 F1200 X79.741 Y117.5 E22.54236
M400
G1 X98.621 Y84.8 E23.79823
M400
G1 X136.379 Y84.8 E25.05406
M400
G1 X155.259 Y117.5 E26.30993
M400
G1 X136.379 Y150.2 E27.5658
M400
G1 X98.621 Y150.2 E28.82164
M400
G0 F6000 X98.852 Y149.8
M400
G1 F1200 X136.148 Y149.8 E30.06211
M400
G1 X154.797 Y117.5 E31.30262
M400
G1 X136.148 Y85.2 E32.54313
M400
G1 X98.852 Y85.2 E33.7836
M400
G1 X80.203 Y117.5 E35.0241
M400
G1 X98.852 Y149.8 E36.26461
M400
G0 F6000 X99.233 Y149.141
M400
G0 X116.925 Y148.233
M400
G0 X117.5 Y147.9
M400
G1 F1200 X91.173 Y102.3 E38.0159
M400
G1 X143.827 Y102.3 E39.76718
M400
G1 X117.5 Y147.9 E41.51846
M400
G0 F6000 X117.5 Y147.1
M400
G1 F1200 X143.134 Y102.7 E43.22366
M400
G1 X91.866 Y102.7 E44.92884
M400
G1 X117.5 Y147.1 E46.63404
M400
;TIME_ELAPSED:73.448151
M140 S0
G91 ;Relative positioning
G1 E-2 F2700 ;Retract a bit
M400
G1 E-2 Z0.2 F2400 ;Retract and raise Z
M400
G1 X5 Y5 F3000 ;Wipe out
M400
G1 Z10 ;Raise Z more
M400
G90 ;Absolute positioning

G1 X0 Y235 ;Present print
M400
M106 S0 ;Turn-off fan
M104 S0 ;Turn-off hotend
M140 S0 ;Turn-off bed

M84 X Y E ;Disable all steppers but Z

M82 ;absolute extrusion mode
M104 S0
;End of Gcode
;SETTING_3 {"global_quality": "[general]\\nversion = 4\\nname = rotating_extrude
;SETTING_3 r_bed_tests\\ndefinition = creality_ender3\\n\\n[metadata]\\ntype = q
;SETTING_3 uality_changes\\nquality_type = standard\\nsetting_version = 20\\n\\n
;SETTING_3 [values]\\nadhesion_type = none\\nmaterial_bed_temperature = 65\\n\\n
;SETTING_3 ", "extruder_quality": ["[general]\\nversion = 4\\nname = rotating_ex
;SETTING_3 truder_bed_tests\\ndefinition = creality_ender3\\n\\n[metadata]\\ntyp
;SETTING_3 e = quality_changes\\nquality_type = standard\\nintent_category = def
;SETTING_3 ault\\nposition = 0\\nsetting_version = 20\\n\\n[values]\\nmagic_mesh
;SETTING_3 _surface_mode = surface\\nmaterial_alternate_walls = True\\nmaterial_
;SETTING_3 print_temperature = 205\\nretraction_enable = False\\nz_seam_corner =
;SETTING_3  z_seam_corner_none\\n\\n"]}
