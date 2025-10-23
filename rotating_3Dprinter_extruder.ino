#include <math.h>

#define PUL 2
#define DIR 4

int rotation_steps = 400; 
float pulley_ratio = 1.6; //32:20
int rotation_limit = round(1*pulley_ratio*rotation_steps); 
int steps_count = 0; 

String cmd; 
int x1 = 0, y1=0;
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
 /* Serial.print("angle: "); 
  Serial.println(angle2); 
  Serial.print("path: ";)
  Serial.println(path);
  Serial.print("steps count: "); 
  Serial.println(steps_count); */
  
  if (Serial.available()) {
    cmd = Serial.readStringUntil('\n');
    x2 = get_pos('X'); 
    y2 = get_pos('Y'); 
    if (cmd.indexOf("G1") != -1 && x2 != -1 && y2 != -1) {
      //if (x2-x1 == 0) angle2 = 0; 
      angle2 = atan2(y2-y1, x2-x1); 
      if (angle2 < 0) angle2 += 2*PI; 
      path = round((angle2 - angle1)*rotation_steps/(2*PI)*pulley_ratio);
      rotate(path); 
      x1 = x2; 
      y1 = y2; 
      angle1 = angle2; 
      steps_count += path; 
    }
  }

  if (abs(steps_count) >= rotation_limit) {
    rotate(-steps_count); 
    steps_count=0; 
  }
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

int optimal_path(int angle2, int angle1) {
  if (angle2 == angle1) return 0; 
  
}





