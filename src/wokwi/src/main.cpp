#include <Arduino.h>
#include <DHT.h>

// Definição dos pinos conectados aos sensores e atuadores
#define PHOSPHORUS_BUTTON_PIN   5   // botão que simula ausência de fósforo quando pressionado
#define POTASSIUM_BUTTON_PIN    4   // botão que simula ausência de potássio quando pressionado
#define PH_SENSOR_PIN           34  // entrada analógica do LDR (simula pH)
#define HUMIDITY_SENSOR_PIN     14  // pino do DHT22 (umidade)
#define RELAY_PIN               2   // LED que simula a bomba d'água
#define DHTTYPE DHT22
DHT dht(HUMIDITY_SENSOR_PIN, DHTTYPE);


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
}

void loop() {
  // Leitura dos botões (pressionado = nutriente ausente)
  bool phosphorusAbsent = digitalRead(PHOSPHORUS_BUTTON_PIN) == LOW;
  bool potassiumAbsent  = digitalRead(POTASSIUM_BUTTON_PIN) == LOW;

  // Leitura do valor do LDR para simular pH (0 a 14)
  int phRaw = analogRead(PH_SENSOR_PIN);
  float phSimulated = (phRaw / 4095.0) * 14.0;

  // Leitura da umidade (%)
  float humidity = dht.readHumidity();

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

  delay(1000);
}
