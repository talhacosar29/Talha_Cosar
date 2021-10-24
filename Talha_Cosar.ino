#define mid_led 5
#define left_led 6
#define right_led 7

int data;

void setup() {
  Serial.begin(9600);
  pinMode(mid_led, OUTPUT);   
  pinMode(left_led, OUTPUT); 
  pinMode(right_led, OUTPUT); 
  Serial.println("Hello World!");

}

void loop() {

  while(Serial.available())
  {
    data = Serial.read();
  }

  if (data == '0')
  {
    digitalWrite(left_led, HIGH);
    digitalWrite(right_led, LOW);
    digitalWrite(mid_led, LOW);
  }

  else if(data == '1')
  {
    digitalWrite(left_led, LOW);
    digitalWrite(right_led, HIGH);
    digitalWrite(mid_led, LOW);
  }
  else if (data == '2')
  {
    digitalWrite(left_led, LOW);
    digitalWrite(right_led, LOW);
    digitalWrite(mid_led, HIGH);
  }
  else if (data == 3)
  {
    digitalWrite(left_led, LOW);
    digitalWrite(right_led, LOW);
    digitalWrite(mid_led, LOW);
  }

}
