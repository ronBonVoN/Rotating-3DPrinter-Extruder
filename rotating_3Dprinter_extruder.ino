#include <math.h>

#define PUL 2 //step pin
#define DIR 8 //direction pin

int rotation_steps = 400; //steps for 2PI rotation
float pulley_ratio = 1.6; //32:20
int rotation_limit = round(1.5*pulley_ratio*rotation_steps); //limit of rotation in single direction
int steps_count = 0;      //steps tracking

String cmd;               //3D printer command 
float x1 = 0.0, y1=0.0;   //previous coordinates
float x2, y2;             //new coordinates
float angle1 = 0.0;       //previous angle
float angle2;             //new angle
int path = 0;             //steps to take from prev angle to new angle

float v;  //nozzel velocity
float fL; //line length without fillet
float fD; //distance covered during fillet
float fR; //fillet radius
float fA; //fillet sweep (angle)
float fC; //fillet direction (cross product)
float d;  //distance nozel has gone
float angle0; 
unsigned long start; //start time (for tracking time)

void rotate(int steps); 
float get_pos(char cor);
void rotate_optimal_path(float angle1, float angle2); 
void print_status(); 

void setup() {
  pinMode(PUL, OUTPUT);
  pinMode(DIR, OUTPUT); 
  Serial.begin(115200);
  print_status();
}

void loop() { 
  
  if (Serial.available()) {
    cmd = Serial.readStringUntil('\n');
    
    x2 = get_pos('X'); 
    y2 = get_pos('Y'); 
    
    v = get_pos('F');
    fL = get_pos('L'); 
    fD = get_pos('D'); 
    fA = get_pos('A'); 
    fC = get_pos('C'); 
    
    if (x2 != -1.0 && y2 != -1.0) {
      start = millis(); 
      angle2 = atan2(y2-y1, x2-x1);
      rotate_optimal_path(angle1, angle2); 
      print_status(); 
      x1 = x2; 
      y1 = y2; 
    }

    if (v != -1.0 && fL != -1.0 && fD != -1.0 && fA != -1.0) {
      Serial.println("FILLET DETECTED");
      while (v*(millis() - start) < fL - fD); 
      Serial.println("FILLET STARTING");
      angle0 = angle1; 
      start = millis(); 
      while (v*(millis() - start) < fD) {
        d = v*(millis() - start);
        if (fR == d) break; 
        angle2 = atan(d/sqrt(fR*fR - d*d)) + PI/2;
        if (fC > 0) angle2 += angle0; 
        if (fC < 0) angle2 = angle0 - angle2; 
        rotate_optimal_path(angle1, angle2); 
        Serial.print("FILLET ");
        print_status(); 
      }
    }
  }

  if (abs(steps_count) >= rotation_limit) {
    rotate(-steps_count); 
    steps_count=0; 
    print_status();
  }
}

void rotate(int steps) {
  if (steps==0) return; 
  digitalWrite(DIR, steps > 0 ? LOW : HIGH);
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
  if (start_idx <= -1 || end_idx <= -1) {
    return -1.0; 
  }
  else {
    return cmd.substring(start_idx + 1, end_idx).toFloat();
  }
}

void rotate_optimal_path(float angle1, float angle2) {
  float dtheta; 
  
  if (angle2 > 2*PI) angle2 -= 2*PI; 
  if (angle2 < 0) angle2 += 2*PI;
  
  if (angle2 == angle1) return 0; 
  if (angle1 > PI && angle2 == 0) angle2 = 2*PI; 
  if (angle2 > PI && angle1 == 0) angle1 = 2*PI; 
  
  if (abs(angle2-angle1) <= abs(angle1-angle2)) dtheta = angle2-angle1; 
  else dtheta = angle1-angle2; 

  path = round(dtheta*rotation_steps/(2*PI)*pulley_ratio);
  rotate(path); 

  angle1 = angle2; 
  steps_count += path;
}

void print_status() {
  Serial.print("angle: ");
  Serial.print(angle1); //state tracking
  Serial.print(" path: ");
  Serial.print(path);
  Serial.print(" steps count: "); 
  Serial.println(steps_count); 
}




