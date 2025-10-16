#include <math.h>

#define PUL 2
#define DIR 4

//extern const char serial_example[]; 
int rotation_steps = 400; 
int rotation_limit = 1*rotation_steps; 
int steps_count = 0; 

bool start = 0; 
String cmd; 
int x1, y1; 
int x2, y2; 
float angle1 = 0; 
float angle2; 
int path = 0; 

void setup() {
  pinMode(PUL, OUTPUT); 
  pinMode(DIR, OUTPUT); 
  Serial.begin(9600);
}

void loop() {
  
  if (!start && Serial.available()) {
    cmd = Serial.readStringUntil('\n');
    x1 = get_pos('X'); 
    y1 = get_pos('Y'); 
    if (cmd.indexOf("G1") != -1 && x1 != -1 && y1 != -1) {
      start = 1; 
    }
  }
  
  if (start && Serial.available()) {
    cmd = Serial.readStringUntil('\n');
    x2 = get_pos('X'); 
    y2 = get_pos('Y'); 
    if (cmd.indexOf("G1") != -1 && x2 != -1 && y2 != -1) {
    rotate(y2); 
      angle2 = atan2(y2-y1, x2-x1); 
      if (angle2 < 0) angle2 += 2*PI; 
      path = round((angle2 - angle1)*rotation_steps/(2*PI));
      rotate(path); 
      x1 = x2; 
      y1 = y2; 
      angle1 = angle2; 
      steps_count += path; 
    }
  }

  if (abs(steps_count) >= rotation_limit) {
    rotate(-steps_count); 
  }
  /*
  -get previous pos
  -get old angle 
  -get currrent pos
  -calc new angle 
    - arctan of change in pos
    - rad%step
  -calc rotation path
    -set direction
      -if (new angle - old angle > 0) ccw
      -if (new andle - old angle < 0) cw
      -if (new angle = old angle) do nothing
    -set rotation path
      -move abs(new angle - old angle)
  */
}

void rotate(int steps) {
  if (steps==0) return; 
  digitalWrite(DIR, steps > 0 ? HIGH : LOW);
  for (int i=0; i<abs(steps); i++) {
    digitalWrite(PUL, HIGH); 
    delay(5);
    digitalWrite(PUL, LOW); 
    delay(5); 
  }
}

int get_pos(char cor) {
  int start_idx = cmd.indexOf(cor);
  int end_idx = cmd.indexOf(' ', start_idx); 
  if (start_idx == -1 || end_idx == -1) {
    return -1; 
  }
  else {
    return cmd.substring(start_idx + 1, end_idx).toInt(); 
  }
}




