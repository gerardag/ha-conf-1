requirements:
	sudo apt install -y jq speedtest-cli bc
	sudo npm i -g mqtt-cli

install: requirements
	sudo mkdir -p /srv/speedtest-to-mqtt
	sudo cp config.json speedtest_mqtt.sh /srv/speedtest-to-mqtt/
	sudo bash -c "echo '*/15 * * * * /bin/bash /srv/speedtest-to-mqtt/speedtest_mqtt.sh' > /etc/cron.d/speedtest_mqtt.cron"