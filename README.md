# Blockchain-ESP32

## ESP32
La scheda che è stata usata per la realizzazione di questo progetto è la ESP32-WROOM-32E con la seguente configurazione dei pin
![BLOCKCHAIN-ESP32](esp32_pinout.png)

### Installazione ambiente e librerie
- Installare Arduino IDE
- Scaricare le librerie:
    - MFRC522 (by Github Developer v.1.4.11)
    - LiquidCrystal (by Arduino Adafruit v.1.0.7)

### Modifica della libreria MFRC522
Per poter usare la libreria MFRC522 con la ESP32 bisogna modificare il file MFRC522Extended.cpp situato nel percorso file Documents\Arduino\libraries\MFRC522\src\MFRC522Extendend.cpp. Bisogna cambiare due righe: 824 e 847.
- rimpiazzare: if (backData && (backlen>0))
- con: if (backData && backlen != nullptr)