
#include <Servo.h>

Servo myservo;  // Membuat objek servo untuk mengontrol servo motor

void setup() {
  Serial.begin(9600);  // Memulai komunikasi serial dengan baud rate 9600
  myservo.attach(9);  // Menghubungkan servo motor ke pin 9
}

void loop() {
  if (Serial.available() > 0) {  // Memeriksa apakah ada data yang tersedia di serial
    int angle = Serial.parseInt();  // Membaca data sudut dari serial
    myservo.write(angle);  // Menggerakkan servo motor sesuai dengan sudut yang diterima
  }
}
