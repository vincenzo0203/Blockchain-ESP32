#include <MFRC522.h>
#include <LiquidCrystal.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

#define GREEN_LED_PIN 16
#define RED_LED_PIN 17

// Modulo RFID
#define SS_PIN  5  
#define RST_PIN 32  

MFRC522 rfid(SS_PIN, RST_PIN);
LiquidCrystal lcd(4, 22, 25, 26, 27, 33);  

int buzzerPin = 21;

const char* ssid = "TIM-19704933 2.4";  
const char* password = "Lqg5J6oXJzcZhxfmUAtG2KFu";  
const char* serverUrl = "https://192.168.1.173:8000/blockchain/check_uid/";  

WiFiClientSecure client;  

void setup() {
  lcd.begin(16, 2);
  lcd.print("Benvenuto");
  SPI.begin();  
  rfid.PCD_Init();
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

  //  Connessione WiFi
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

  //  Carica il certificato SSL
  client.setInsecure(); //client.setCACert(root_ca); 
}
 
void loop() {
  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
    String uid = getUID();
    if (checkUID(uid)) {
      blinkLed(GREEN_LED_PIN, 2000, 1);
      lcd.setCursor(4, 0);
      lcd.print("Accesso");
      lcd.setCursor(3, 1);
      lcd.print("Consentito");
    } else {
      blinkLed(RED_LED_PIN, 400, 2);
      lcd.setCursor(4, 0);
      lcd.print("Accesso");
      lcd.setCursor(5, 1);
      lcd.print("Negato");
      tone(buzzerPin, 1000, 500);
    }
  }
  delay(2000);
  lcd.clear();
}

String getUID() {
  String uid = "";
  for (int i = 0; i < rfid.uid.size; i++) {
    uid += rfid.uid.uidByte[i] < 0x10 ? "0" : "";
    uid += String(rfid.uid.uidByte[i], HEX);
  }
  rfid.PICC_HaltA();
  return uid;
}

bool checkUID(String uid) {
  if (WiFi.status() != WL_CONNECTED) {
    lcd.setCursor(0, 1);
    lcd.print("WiFi disconnesso");
    return false;
  }

  HTTPClient https;
  https.begin(client, serverUrl);  
  https.addHeader("Content-Type", "application/json");

  String jsonPayload = "{\"uid\": \"" + uid + "\"}";
  int httpResponseCode = https.POST(jsonPayload);

  if (httpResponseCode > 0) {
    String response = https.getString();
    https.end();

    DynamicJsonDocument doc(1024);
    DeserializationError error = deserializeJson(doc, response);
    if (error) return false;

    return doc["access"];
  } else {
    https.end();
    return false;
  }
}

void blinkLed(int led, int duration, int repeat) {
  for (int i = 0; i < repeat; i++) {
    digitalWrite(led, HIGH);
    delay(duration / 2);
    digitalWrite(led, LOW);
    delay(duration / 2);
  }
}
