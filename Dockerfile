FROM arm64v8/python
COPY /src /app
RUN apt-get -qq update && python -m pip install --upgrade pip && pip install paho-mqtt && pip install RPi.GPIO && pip install Adafruit_DHT && pigpiod && pip install pigpio-dht
WORKDIR /app
CMD ["python3", "terrarium_monitor.py"]