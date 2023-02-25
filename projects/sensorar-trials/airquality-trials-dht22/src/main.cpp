// dependências sobre framework arduino e placa Heltec
#include <Arduino.h>
#include <heltec.h>

// dependências sobre sensores Adafruit
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

// definição de modelo do sensor e de pino utilizado para dados
#define DHTPIN 4
#define DHTTYPE DHT22

// instância manipulador do sensor DHT22
DHT_Unified dht(DHTPIN, DHTTYPE);

void setup()
{
	// inicializa o funcionamento da porta serial
	Serial.begin(9600);

	// configura DHT22 antes da inicialização 
	sensor_t sensor;
	dht.temperature().getSensor(&sensor);
	dht.humidity().getSensor(&sensor);

	// inicializa funcionamento do DHT22
	dht.begin();
}

void loop()
{

	// estabelece delay entre leituras
	delay(3000);

	// declara objeto evento para a captura das leituras
	sensors_event_t event;
	
	// declara variáveis utilizadas para armazenamento temporário e flags
	float temp, rh;
	bool hasReadTemp = false, hasReadRH = false;

	// tenta capturar leituras de temperatura no objeto evento
	dht.temperature().getEvent(&event);
	delay(1000);
	if (!isnan(event.temperature))
	{
		temp = event.temperature;
		hasReadTemp = true;
	}

	// tenta capturar leituras de umidade relativa no objeto evento
	dht.humidity().getEvent(&event);
	delay(1000);
	if (!isnan(event.relative_humidity))
	{
		rh = event.relative_humidity;
		hasReadRH = true;
	}

	// verifica se os dois valores foram capturados com sucesso e imprime-os na tela
	if(hasReadTemp && hasReadRH)
	{
		Serial.print(F("{ \"temp\": "));
		Serial.print(temp);
		Serial.print(F(", \"rh\": "));
		Serial.print(rh);
		Serial.println(F(" }"));
	} else
		Serial.println(F("Erro na leitura do sensor!"));
}