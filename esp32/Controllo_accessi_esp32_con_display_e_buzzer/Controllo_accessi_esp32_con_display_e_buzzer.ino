#include <MFRC522.h>
#include <LiquidCrystal.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

/**
* Source code:
* https://www.italiantechproject.it/sensori-con-arduino/lettore-rfid
* For more detail (instruction and wiring diagram), visit https://esp32io.com/tutorials/esp32-rfid-nfc
* For more detail Lab 14 (esp32 lcd 16x2 without I2C https://deepbluembedded.com/esp32-lcd-display-16x2-without-i2c-arduino/?utm_content=cmp-true)
*/

#define GREEN_LED_PIN 16
#define RED_LED_PIN 17

//per modulo RFID
#define SS_PIN  5  // ESP32 pin GPIO5 
#define RST_PIN 32 // ESP32 pin GPIO27
 
MFRC522 rfid(SS_PIN, RST_PIN);

LiquidCrystal lcd(4, 22, 25, 26, 27, 33);  // RS, EN, D4, D5, D6, D7
 
//String users[] = {"f3620c35"};
//int usersSize = sizeof(users)/sizeof(String);

int buzzerPin = 21;

const char* ssid = "TIM-19704933 2.4"; // Sostituisci con il nome della tua rete WiFi
const char* password = "Lqg5J6oXJzcZhxfmUAtG2KFu"; // Sostituisci con la password della tua rete WiFi
const char* serverUrl = "http://192.168.1.173:8000/blockchain/check_uid/"; // URL del tuo backend Python


//testo pe il display
String text = "Accesso";
int col = 4;

String text_red = "Negato";
int col_red = 5;

String text_green = "Consentito";
int col_green = 3;
 
void setup(){
  lcd.begin(16, 2);
  lcd.print("Benvenuto");
  SPI.begin();  //da verificare se serve o meno
  rfid.PCD_Init();
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

  // Connessione WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    lcd.setCursor(0, 1);
    lcd.print("Connessione...");
  }
  lcd.clear();
  lcd.print("WiFi Connesso");
  delay(2000);
  lcd.clear();
}
 
void loop(){
  if(rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()){
    String uid = getUID();
    if(checkUID(uid)){
      blinkLed(GREEN_LED_PIN, 2000, 1);

      //per il testo sul display in caso positivo
      lcd.setCursor(col, 0);
      lcd.print(text);
      lcd.setCursor(col_green, 1);
      lcd.print(text_green);
    }else{
      blinkLed(RED_LED_PIN, 400, 2);

      //per il testo sul display in caso negativo
      lcd.setCursor(col, 0);
      lcd.print(text);
      lcd.setCursor(col_red, 1);
      lcd.print(text_red);
      tone(buzzerPin, 1000, 500);
    }
  }
  delay(2000);
  lcd.clear();
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
  /*for(int i = 0; i < usersSize; i++){
    if(users[i] == uid){
      return true;
    }
  }
  return false;*/
  if (WiFi.status() != WL_CONNECTED) {
    lcd.setCursor(0, 1);
    lcd.print("WiFi disconnesso");
    return false;
  }

  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");

  // Prepara il payload JSON con l'UID
  String jsonPayload = "{\"uid\": \"" + uid + "\"}";
  int httpResponseCode = http.POST(jsonPayload);

  if (httpResponseCode > 0) {
    // Leggi la risposta del server
    String response = http.getString();
    http.end();

    // Decodifica la risposta JSON
    DynamicJsonDocument doc(1024);
    DeserializationError error = deserializeJson(doc, response);

    if (error) {
      lcd.setCursor(0, 1);
      lcd.print("Errore JSON");
      delay(2000);
      lcd.clear();
      return false;
    }

    // Controlla il valore di "access"
    bool access = doc["access"];
    return access;
  } else {
    // Gestisce errori HTTP
    lcd.setCursor(0, 1);
    lcd.print("Errore HTTP: ");
    lcd.print(httpResponseCode);
    http.end();
    delay(2000);
    lcd.clear();
    return false;
  }
}
 
void blinkLed(int led, int duration, int repeat){
  for(int i = 0; i < repeat; i++){
    digitalWrite(led, HIGH);
    delay(duration/2);
    digitalWrite(led, LOW);
    delay(duration/2);
  }
}
