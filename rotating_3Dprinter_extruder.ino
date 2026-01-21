#include <math.h>

#define PUL 2 //step pin
#define DIR 8 //direction pin
#define MIN_STEP_PERIOD 2.0 //ms 
#define ROTATION_STEPS 400 //steps for 2PI rotation
#define PULLEY_RATIO 1.6 //32:20

int rotation_limit = round(1.5*PULLEY_RATIO*ROTATION_STEPS); //limit of rotation in single direction
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

void rotate(int steps, float step_period);
float get_pos(char cor);
void rotate_optimal_path(float &angle1, float angle2); 
void check_rotation_limit(); 
void print_status(); 

void setup() {
  pinMode(PUL, OUTPUT);
  pinMode(DIR, OUTPUT); 
  Serial.begin(115200);
  print_status();
}

void loop() { 
  
  if (Serial.available()) cmd = Serial.readStringUntil('\n');
  else return; 
    
  x2 = get_pos('X'); y2 = get_pos('Y');    
  if (isnan(x2) && isnan(y2)) return; 
  else {
    start = millis(); 
    angle2 = atan2(y2-y1, x2-x1);
    rotate_optimal_path(angle1, angle2, MIN_STEP_PERIOD); 
    print_status();
    x1 = x2; 
    y1 = y2; 
  }

  v = get_pos('F'); fL = get_pos('L'); fD = get_pos('D'); fR = get_pos('R');fA = get_pos('A'); fC = get_pos('C'); 
  if (isnan(v) && isnan(fL) && isnan(fD) && isnan(fR) && isnan(fA)) return; 
  else {
    Serial.println("FILLET DETECTED"); 
    if (fC < 0) angle2 = angle1 - fA; 
    else angle2 = angle1 + fA; 
    while (v*(millis() - start)/1000.0/60.0 < fL - fD); 
    rotate_optimal_path(angle1, angle2, fR/v/60.0*1000.0); 
  }
}

void rotate(int steps, float step_period) {
  if (step_period < MIN_STEP_PERIOD) step_period = MIN_STEP_PERIOD; 
  digitalWrite(DIR, steps > 0 ? LOW : HIGH);
  for (int i=0; i<abs(steps); i++) {
    digitalWrite(PUL, HIGH); 
    delay(step_period/2);
    digitalWrite(PUL, LOW); 
    delay(step_period/2); 
  }
}

float get_pos(char cor) {
  int start_idx = cmd.indexOf(cor);
  int end_idx = cmd.indexOf(' ', start_idx); 
  if (start_idx <= -1 || end_idx <= -1) {
    return NAN; 
  }
  else {
    return cmd.substring(start_idx + 1, end_idx).toFloat();
  }
}

void rotate_optimal_path(float &angle1, float angle2, float step_period) {
  float dtheta; 
  
  if (angle2 > 2*PI) angle2 -= 2*PI; 
  if (angle2 < 0) angle2 += 2*PI;
  
  if (angle1 > PI && angle2 == 0) angle2 = 2*PI; 
  if (angle2 > PI && angle1 == 0) angle1 = 2*PI; 
  
  if (abs(angle2-angle1) <= abs(angle1-angle2)) dtheta = angle2-angle1; 
  else dtheta = angle1-angle2; 

  path = round(dtheta*ROTATION_STEPS/(2*PI)*PULLEY_RATIO);

  if (path != 0) {
    angle1 = angle2; 
    rotate(path, step_period); 
    steps_count += path;
    print_status(); 
    check_rotation_limit(); 
  }
}

void check_rotation_limit() {
  if (abs(steps_count) >= rotation_limit) {
  rotate(-steps_count, MIN_STEP_PERIOD); 
  steps_count=0; 
  print_status();
  }
}

void print_status() {
  Serial.print("angle: ");
  Serial.print(angle1); //state tracking
  Serial.print(" path: ");
  Serial.print(path);
  Serial.print(" steps count: "); 
  Serial.println(steps_count); 
}




