#include <MFRC522.h>
#include <LiquidCrystal.h>

/**
* Source code:
* https://www.italiantechproject.it/sensori-con-arduino/lettore-rfid
* For more detail (instruction and wiring diagram), visit https://esp32io.com/tutorials/esp32-rfid-nfc
* For more detail Lab 14 (esp32 lcd 16x2 without I2C https://deepbluembedded.com/esp32-lcd-display-16x2-without-i2c-arduino/?utm_content=cmp-true)
*/

#define GREEN_LED_PIN 32
#define RED_LED_PIN 4

//per modulo RFID
#define SS_PIN  5  // ESP32 pin GPIO5 
#define RST_PIN 27 // ESP32 pin GPIO27
 
MFRC522 rfid(SS_PIN, RST_PIN);

LiquidCrystal My_LCD(14, 13, 17, 26, 25, 33);  // RS, EN, D4, D5, D6, D7
 
String users[] = {"f3620c35"};
int usersSize = sizeof(users)/sizeof(String);

int buzzerPin = 16;
 
void setup(){
  SPI.begin();  //da verificare se serve o meno
  rfid.PCD_Init();
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

  My_LCD.begin(16, 2);
  My_LCD.print("AAAAA");
}
 
void loop(){
  if(rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()){
    String uid = getUID();
    if(checkUID(uid)){
      blinkLed(GREEN_LED_PIN, 2000, 1);
      My_LCD.print("Accesso consentito");
    }else{
      blinkLed(RED_LED_PIN, 400, 2);
      My_LCD.print("Accesso negato");
      tone(buzzerPin, 1000, 500);
    }
  }
  delay(10);
  My_LCD.clear();
}
 
String getUID(){
  String uid = "";
  for(int i = 0; i < rfid.uid.size; i++){
    uid += rfid.uid.uidByte[i] < 0x10 ? "0" : "";
    uid += String(rfid.uid.uidByte[i], HEX);
  }
  rfid.PICC_HaltA();
  return uid;
}
 
bool checkUID(String uid){
  for(int i = 0; i < usersSize; i++){
    if(users[i] == uid){
      return true;
    }
  }
  return false;
}
 
void blinkLed(int led, int duration, int repeat){
  for(int i = 0; i < repeat; i++){
    digitalWrite(led, HIGH);
    delay(duration/2);
    digitalWrite(led, LOW);
    delay(duration/2);
  }
}
