#include <math.h>

#define PUL 2 //step pin
#define DIR 4 //direction pin

int rotation_steps = 400; //steps for 2PI rotation
float pulley_ratio = 1.6; //32:20
int rotation_limit = round(1*pulley_ratio*rotation_steps); //limit of rotation in single direction
int steps_count = 0; //steps tracking

String cmd;             //3D printer command 
float x1 = 0.0, y1=0.0; //previous coordinates
float x2, y2;           //new coordinates
float angle1 = 0.0;     //previous angle
float angle2;           //new angle
int path = 0;           //steps to take from prev angle to new angle
bool pre_heater = 1;

void setup() {
  pinMode(PUL, OUTPUT);
  pinMode(DIR, OUTPUT); 
  Serial.begin(9600);
}

void loop() { 
  Serial.print("angle: "); //state tracking
  Serial.print(angle1); 
  Serial.print(" path: ");
  Serial.print(path);
  Serial.print(" steps count: "); 
  Serial.println(steps_count); 
  
  if (Serial.available()) {
    cmd = Serial.readStringUntil('\n');
    x2 = get_pos('X'); 
    y2 = get_pos('Y'); 
    if (cmd.indexOf("G1") != -1 && x2 != -1 && y2 != -1) {
      angle2 = atan2(y2-y1, x2-x1); //rangle -PI to PI
      if (angle2 < 0) angle2 += 2*PI; //range 0 to 2PI
      path = round((optimal_path_angle(angle1, angle2))*rotation_steps/(2*PI)*pulley_ratio);
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
    delay(2);
    digitalWrite(PUL, LOW); 
    delay(2); 
  }
}

float get_pos(char cor) {
  int start_idx = cmd.indexOf(cor);
  int end_idx = cmd.indexOf(' ', start_idx); 
  if (start_idx == -1 || end_idx == -1) {
    return -1; 
  }
  else {
    return cmd.substring(start_idx + 1, end_idx).toFloat();
  }
}

float optimal_path_angle(float angle1, float angle2, bool switching=0) {
  if (angle2 == angle1) return 0.0; 
  
  if (angle1 > PI && angle2 == 0) angle2 = 2*PI; 
  if (angle2 > PI && angle1 == 0) angle1 = 2*PI; 

  if (switching) {
    if (angle2 == angle1 + PI) {
      angle2 = angle1;
      pre_heater = !pre_heater; 
    }
         /* if (abs(angle2 - angle1) == PI/2) {
        angle2 = -angle2; 
        pre_heater = 0; 
      }
      else if (angle2 == angle1 + PI) { //don't move if angles are opisite
        angle2 = angle1;
        pre_heater = !pre_heater; 
      }
      else if (abs(angle2 - angle1) >= abs(angle2 + PI - angle1)) { //use inverse angle is a shorter distance
        angle2 += PI;
        pre_heater = !pre_heater; 
      }*/
  }
  
  if (abs(angle2-angle1) <= abs(angle1-angle2)) return angle2-angle1; 
  else return angle1-angle2; 


}




