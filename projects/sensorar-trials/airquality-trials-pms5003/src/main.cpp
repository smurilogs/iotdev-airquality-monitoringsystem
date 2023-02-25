// dependências sobre framework arduino e placa Heltec
#include <Arduino.h>
#include <heltec.h>

// dependências para manipulação do PMS5003
#include <Adafruit_Sensor.h>
#include <Adafruit_PM25AQI.h>
#include <PMS.h>

//
PMS pms(Serial2);
PMS::DATA data;

void setup()
{
	// inicializa interface serial utilizada para comunicação com o terminal 
	Serial.begin(9600);
	
	// inizializa interface serial utilizada para comunicação com o PMS5003
	Serial2.begin(9600, SERIAL_8N1, 33, 32);
	
	// inicializa e configura o PMS5003 para atuar no modo passivo
	pms.passiveMode();
}

void loop()
{
	// acorda o PMS5003, ativando seu fluxo de ar por 30 segundos para preparar o sensor para a próxima leitura
	pms.wakeUp();
	delay(30000);

	// requisita a leitura do PMS5003
	pms.requestRead();

	// espera por um segundo a chegada da resposta com a leitura
	if (pms.readUntil(data))
	{
		//Serial.print("PM 1.0 (ug/m3): ");
		//Serial.println(data.PM_AE_UG_1_0);
		////Serial.println(data.PM_SP_UG_1_0);

		//Serial.print("PM 2.5 (ug/m3): ");
		//Serial.println(data.PM_AE_UG_2_5);    
		////Serial.println(data.PM_SP_UG_2_5);

		//Serial.print("PM 10.0 (ug/m3): ");
		//Serial.println(data.PM_AE_UG_10_0);
		////Serial.println(data.PM_SP_UG_10_0);
		
		Serial.print(F("{ \"pm1_0\": "));
		Serial.print(data.PM_AE_UG_1_0);

		Serial.print(F(", \"pm2_5\": "));
		Serial.print(data.PM_AE_UG_2_5);
		
		Serial.print(F(", \"pm10_0\": "));
		Serial.print(data.PM_AE_UG_10_0);
		Serial.println(F(" }"));
	}
	else
		Serial.println("Erro na leitura do sensor!");
	
	pms.sleep();
	delay(30000);
}