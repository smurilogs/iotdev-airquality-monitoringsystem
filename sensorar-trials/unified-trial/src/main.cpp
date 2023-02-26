// dependências sobre framework arduino e placa Heltec
#include <Arduino.h>
#include <heltec.h>

// dependências para manipulação dos sensores
#include <Adafruit_Sensor.h>
#include <Adafruit_PM25AQI.h>
#include <DHT.h>
#include <DHT_U.h>
#include <PMS.h>

// definição de modelo do sensor e de pino utilizado para dados
#define DHTPIN 4
#define DHTTYPE DHT22

// objetos globais para manipulação do DHT22
DHT_Unified dht(DHTPIN, DHTTYPE);
sensor_t sensor;

// objetos globais para manipulação do PMS5003
PMS pms(Serial2);
PMS::DATA data;

void setup()
{
	// inicializa o funcionamento da porta serial
	Serial.begin(9600);

	// utiliza o objeto sensor para configurar e inicializar o funcionamento do DHT22 
	dht.temperature().getSensor(&sensor);
	dht.humidity().getSensor(&sensor);
	dht.begin();

	// inicializa interface UART2 do ESP32, utilizando os pinos 32 (TX) e 33 (RX)
	Serial2.begin(9600, SERIAL_8N1, 33, 32);

	// configura o PMS5003 no modo passivo inicia sua operação no modo awake 
	pms.passiveMode();
	pms.wakeUp();
}

void loop()
{
	// declara objeto evento para a captura das leituras
	sensors_event_t event;

	// declara variáveis utilizadas para armazenamento temporário e flags
	float temp, rh;
	uint16_t pm10_0, pm2_5, pm1_0;
	bool hasReadTemp = false, hasReadRH = false, hasReadPM = false;

	// acorda o PMS5003, ativando seu fluxo de ar por 30 segundos 
	// para preparar o sensor para a próxima leitura
	pms.wakeUp();
	delay(15000);

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

	// espera por um segundo a chegada da resposta com a leitura
	if(pms.readUntil(data))
	{
		pm1_0 = data.PM_AE_UG_1_0;
		pm2_5 = data.PM_AE_UG_2_5;
		pm10_0 = data.PM_AE_UG_10_0;
		hasReadPM = true;
	}

	// verifica se os dois valores foram capturados com
	// sucesso e apresenta-os no terminal serial
	if(hasReadTemp && hasReadRH && hasReadPM)
	{
		Serial.print(F("{ \"temp\": "));
		Serial.print(temp);
		Serial.print(F(", \"rh\": "));
		Serial.print(rh);
		Serial.print(F(", \"pm1_0\": "));
		Serial.print(pm1_0);
		Serial.print(F(", \"pm2_5\": "));
		Serial.print(pm2_5);
		Serial.print(F(", \"pm10_0\": "));
		Serial.print(pm10_0);
		Serial.println(F(" }"));
	} else
		Serial.println(F("Erro na leitura do sensor!"));

	// coloca o PMS5003 no modo sleep por 30 segundos
	pms.sleep();
	delay(15000);
}