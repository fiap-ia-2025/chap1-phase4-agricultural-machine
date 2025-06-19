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

unsigned long lastUpdate = 0; // Variável para controlar o tempo de atualização do LCD
uint32_t interval = 500; // Intervalo de atualização do LCD em milissegundos

void setup() {
  Serial.begin(115200);  // inicia comunicação com o monitor serial

  // Configura botões com resistência interna pull-up (pressionado = LOW = nutriente ausente)
  pinMode(PHOSPHORUS_BUTTON_PIN, INPUT_PULLUP);
  pinMode(POTASSIUM_BUTTON_PIN, INPUT_PULLUP);

  // Configura relé (LED) como saída
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);  // bomba começa desligada

  // Inicializa o sensor de umidade
  dht.begin(); 

  // Inicializa o LCD
  lcd.init();
  lcd.backlight();
  Serial.println("Sistema de Irrigação Inicializado");
}

void loop() {

  // Atualiza o LCD a cada intervalo definido
  unsigned long currentMillis = millis();
  
  // Verifica se o tempo atual menos o tempo da última atualização é maior ou igual ao intervalo
  // Se for, atualiza o LCD e lê os sensores
  // Isso evita que o LCD seja atualizado a cada iteração do loop, economizando recursos
  // e permitindo que o sistema responda a outras tarefas, como leituras de sensores e
  // acionamento de atuadores, sem atrasos significativos.
  // Isso também garante que o LCD seja atualizado em intervalos regulares, conforme definido pela
  if (currentMillis - lastUpdate >= interval) {
    lastUpdate = currentMillis; // Atualiza o tempo da última atualização do LCD  

    // Leitura dos botões (pressionado = nutriente ausente)
    bool phosphorusAbsent = digitalRead(PHOSPHORUS_BUTTON_PIN) == LOW;
    bool potassiumAbsent  = digitalRead(POTASSIUM_BUTTON_PIN) == LOW;

    // Leitura do valor do LDR para simular pH (0 a 14)
    int phRaw = analogRead(PH_SENSOR_PIN);
    float phSimulated = (phRaw / 4095.0) * 14.0;

    // Leitura da umidade (%)
    float humidity = dht.readHumidity();

    // Verifica se a leitura de umidade falhou
    if (isnan(humidity)) {
      Serial.println("Falha ao ler umidade!");
      humidity = 0;  // Define umidade como 0 em caso de falha
    }

    // Mostra informações no monitor serial
    Serial.print("P=");
    Serial.print(phosphorusAbsent ? "Ausente" : "Presente");
    Serial.print(", K=");
    Serial.print(potassiumAbsent ? "Ausente" : "Presente");
    Serial.print(", Umidade=");
    Serial.print(humidity);
    Serial.print("%, pH=");
    Serial.print(phSimulated, 1);

    // Aciona bomba somente se umidade estiver abaixo de 40%, 1 = Ligada e 0 = Desligada
    bool shouldIrrigate = humidity < 40;

    digitalWrite(RELAY_PIN, shouldIrrigate ? HIGH : LOW);

    if (shouldIrrigate) {
      Serial.println(", Bomba=1");
    } else {
      Serial.println(", Bomba=0");
    }

    // Exibe informações no LCD
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Umi:");
    lcd.print(humidity, 1);
    lcd.print("% pH:");
    lcd.print(phSimulated, 1);

    lcd.setCursor(0, 1);
    lcd.print("P:");
    lcd.print(phosphorusAbsent ? "A" : "P");
    lcd.print(" K:");
    lcd.print(potassiumAbsent ? "A" : "P");
    lcd.print(" B:");
    lcd.print(shouldIrrigate ? "1" : "0");

  } // Fim da atualização do LCD
  // Aguarda um pouco antes da próxima iteração do loop
  delay(100); // Pequeno atraso para evitar sobrecarga do loop
}