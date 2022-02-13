# pull mqtt image from docker hub
FROM eclipse-mosquitto:2.0.10

# set provisional password
RUN touch /mosquitto/passwd
RUN mosquitto_passwd -b /mosquitto/passwd dso_server dso_password

EXPOSE 1883