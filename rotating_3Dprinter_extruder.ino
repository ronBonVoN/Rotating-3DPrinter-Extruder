#include <math.h>

#define PUL 2 //step pin
#define DIR 8 //direction pin
#define MAX_ROTATION 1 //1 is full rotation
#define MIN_STEP_PERIOD 2 //ms
#define ROTATION_STEPS 400 //steps for 2PI rotation
#define PULLEY_RATIO 1.6 //32:20

const int rotation_limit = round(MAX_ROTATION*PULLEY_RATIO*ROTATION_STEPS); //limit of rotation in single direction
const float rotation_ratio = ROTATION_STEPS/(2*PI)*PULLEY_RATIO; 
int steps_count = 0; //steps tracking
int path = 0;        //steps to take from prev angle to new angle
int step_period;     //rotation rate 

String cmd;          //rotation command 
float angle1 = 0.0;  //previous angle
float angle2;        //new angle
float dtheta;        //change in angle 

void rotate(int steps, int step_period);
float get_pos(char cor);

void setup() {
  pinMode(PUL, OUTPUT);
  pinMode(DIR, OUTPUT); 
  Serial.begin(115200);
}

void loop() { 
  if (Serial.available()) cmd = Serial.readStringUntil('\n');
  else return; 

  if (isnan(get_pos('A')) && isnan(get_pos('P'))) return; 

  angle2 = get_pos('A'); 
  dtheta = dtheta = atan2(sin(angle2 - angle1), cos(angle2 - angle1));
  path = round(dtheta*rotation_ratio);
  angle1 = angle2; 

  step_period = round(get_pos('P')/rotation_ratio);
  if (step_period < MIN_STEP_PERIOD) step_period = MIN_STEP_PERIOD; 
  rotate(path, step_period);

  steps_count += path;  
  if (abs(steps_count) >= rotation_limit) {
    rotate(-steps_count, MIN_STEP_PERIOD); 
    steps_count=0; 
  }

  Serial.print("angle:");
  Serial.print(angle1);
  Serial.print(" steps_count:"); 
  Serial.print(steps_count); 
  Serial.print(" step_period:");
  Serial.println(step_period);
}

void rotate(int steps, int step_period) {
  int pull_delay = round(step_period/2); 
  digitalWrite(DIR, steps > 0 ? LOW : HIGH);
  for (int i=0; i<abs(steps); i++) {
    digitalWrite(PUL, HIGH); 
    delay(pull_delay);
    digitalWrite(PUL, LOW); 
    delay(pull_delay); 
  }
}

float get_pos(char cor) {
  int start_idx = cmd.indexOf(cor);
  int end_idx = cmd.indexOf(' ', start_idx); 
  if (end_idx == -1) end_idx = cmd.length(); 
  if (start_idx <= -1 || end_idx <= -1) return NAN; 
  else return cmd.substring(start_idx + 1, end_idx).toFloat();
}




