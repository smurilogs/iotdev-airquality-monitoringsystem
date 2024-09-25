

## Summary

This repository contains the code and documentation of the final project that presents an architecture and development proposal for an IoT system to monitor air quality in the Araripe Gypsum Hub region, using LoRa and LoRaWAN technologies.

The proposed system monitors the presence of particulate matter (PM10 and PM2.5) suspended in the air, collecting data that can be stored and analyzed later. The project was developed in a controlled environment to test the feasibility of using LoRaWAN for this application, with potential application in the Araripe Gypsum Hub.

## Objectives

### General Objective
To develop an IoT system to monitor particulate matter (PM10 and PM2.5) in areas impacted by gypsum production, such as the Araripe Gypsum Hub.

### Specific Objectives
- Develop and test a prototype to capture data on pollutants and environmental conditions.
- Implement LoRaWAN communication between sensors and the gateway.
- Develop an application for visualization and analysis of the collected data.

## Technologies Used

- **LoRa/LoRaWAN:** Long-range, low-power wireless communication technology.
- **Sensors:** DHT22 for temperature and humidity, PMS5003 for PM10 and PM2.5 detection.
- **Development Platform:** Heltec WiFi LoRa 32.
- **The Things Stack (TTS) Community Edition:** Platform for managing LoRaWAN devices.
- **Python (Pandas and Streamlit):** For data analysis and presentation.

## System Architecture

The system is composed of:
1. **End-device**: Equipment with sensors for temperature, humidity, and particulate matter.
2. **LoRaWAN Gateway**: Receives data from end-devices and transmits it to the network.
3. **TTS (The Things Stack)**: LoRaWAN network server that processes and stores the data.
4. **Web Application**: Interface for visualizing and analyzing the collected data.

## Configuration

### Requirements

- **PlatformIO** (VSCode) development platform
- **Heltec WiFi LoRa 32** device
- **DHT22** and **PMS5003** sensors
- An account on **The Things Stack Community Edition**

### Configuration Steps

1. Set up the hardware and integrate the sensors with the Heltec WiFi LoRa 32 board.
2. Configure the LoRaWAN gateway (e.g., Dragino LPS8) to communicate with the TTS server.
3. Register the end-devices and create an application on the TTS console.
4. Develop the application to collect and visualize data using **Streamlit** and **Pandas**.

## Results

The feasibility of using LoRaWAN for monitoring particulate matter was confirmed through tests with sensors and data transmission in a controlled environment.

## Future Improvements

- Expand the network coverage by installing more gateways in the Araripe region.
- Optimize the energy consumption of the end-devices.
- Expand the system to monitor other atmospheric pollutants.
