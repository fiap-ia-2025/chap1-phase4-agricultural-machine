#include <Arduino.h>
#include <DHT.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Definição dos pinos conectados aos sensores e atuadores
#define PHOSPHORUS_BUTTON_PIN   5   // botão que simula ausência de fósforo quando pressionado
#define POTASSIUM_BUTTON_PIN    4   // botão que simula ausência de potássio quando pressionado
#define PH_SENSOR_PIN           34  // entrada analógica do LDR (simula pH)
#define HUMIDITY_SENSOR_PIN     14  // pino do DHT22 (umidade)
#define RELAY_PIN               2   // LED que simula a bomba d'água
#define DHTTYPE DHT22
DHT dht(HUMIDITY_SENSOR_PIN, DHTTYPE);

// LCD I2C: endereço 0x27, 16 colunas, 2 linhas
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Otimização: intervalos pequenos podem ser uint16_t (até 65535 ms)
unsigned long lastUpdate = 0; // Mantém unsigned long para millis()
const uint16_t interval = 500; // Intervalo de atualização do LCD em milissegundos

void setup() {
  Serial.begin(115200);

  pinMode(PHOSPHORUS_BUTTON_PIN, INPUT_PULLUP);
  pinMode(POTASSIUM_BUTTON_PIN, INPUT_PULLUP);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);

  dht.begin();
  lcd.init();
  lcd.backlight();

  Serial.println("Sistema de Irrigação Inicializado");
}

void loop() {
  unsigned long currentMillis = millis();

  // Verifica se o intervalo de atualização foi atingido
  // Otimização: evita cálculos desnecessários se o intervalo não foi atingido
  // Isso reduz a carga no loop principal, especialmente em sistemas com recursos limitados
  // e melhora a responsividade do sistema.
  // A verificação de tempo é feita apenas uma vez por iteração do loop
  // para evitar múltiplas leituras de sensores e atualizações de LCD desnecessárias
  if (currentMillis - lastUpdate >= interval) {
    lastUpdate = currentMillis;

    // Otimização: bool ocupa 1 byte, ideal para flags
    bool phosphorusAbsent = digitalRead(PHOSPHORUS_BUTTON_PIN) == LOW;
    bool potassiumAbsent  = digitalRead(POTASSIUM_BUTTON_PIN) == LOW;

    // Otimização: int16_t suficiente para analogRead (0-4095)
    int16_t phRaw = analogRead(PH_SENSOR_PIN);

    float phSimulated = (phRaw / 4095.0f) * 14.0f;
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();


    if (isnan(humidity) || isnan(temperature)) {
      Serial.println("Falha ao ler sensores de umidade e temperatura!");
      return; // Sai do loop se a leitura falhar
    }

    // Otimização: char para status simples
    char phosphorusStatus = phosphorusAbsent ? 'A' : 'P';
    char potassiumStatus  = potassiumAbsent  ? 'A' : 'P';

    // Otimização: bool para status da bomba
    bool shouldIrrigate = humidity < 40.0f;

    digitalWrite(RELAY_PIN, shouldIrrigate ? HIGH : LOW);

    // Exibe informações no Serial Monitor 
    Serial.print("Umi: ");
    Serial.print((uint8_t)humidity); // uint8_t suficiente para 0-100%
    Serial.print("% pH: ");
    Serial.print(phSimulated, 1);
    Serial.print(" Temp: ");
    Serial.print((uint8_t)temperature);
    Serial.print(" P: ");
    Serial.print(phosphorusStatus);
    Serial.print(" K: ");
    Serial.print(potassiumStatus);
    Serial.print(" B: ");
    Serial.println(shouldIrrigate ? "1" : "0");
    
    // Exibe informações no Serial Monitor em formato CSV
    // Serial.print(humidity, 1); Serial.print(",");
    // Serial.print(phSimulated, 2); Serial.print(",");
    // Serial.print(temperature, 1); Serial.print(",");
    // Serial.print(phosphorusStatus); Serial.print(",");
    // Serial.print(potassiumStatus); Serial.print(",");
    // Serial.println(shouldIrrigate ? "1" : "0");

    // Exibe informações no LCD
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Umi:");
    lcd.print((uint8_t)humidity); // uint8_t suficiente para 0-100%
    lcd.print("% pH:");
    lcd.print(phSimulated, 1);

    lcd.setCursor(0, 1);
    lcd.print("T:");
    lcd.print((uint8_t)temperature);
    lcd.print(" P:");
    lcd.print(phosphorusStatus);
    lcd.print(" K:");
    lcd.print(potassiumStatus);
    lcd.print(" B:");
    lcd.print(shouldIrrigate ? '1' : '0');

  }
  delay(100); // Pequeno atraso para evitar sobrecarga do loop
}