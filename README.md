# Weather station with Raspberry PI and Google cloud

Complete implementation of a weather station with GPS, a LCD screen, and a sensor of humidity
and temperature. The implementation consists in the station and a server in google cloud
consisting of multiple services. These are the web to check the measurements, the message
router and broker with MQTT, the python code to process the messages and a MariaDB to save
the measurements. All this managed with docker.