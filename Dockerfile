FROM arm64v8/python
COPY /src /app
RUN apt-get -qq update && python -m pip install --upgrade pip && apt-get install -y python3-pip && pip install -y paho-mqtt && pip install -y RPi.GPIO
RUN python3 -m pip install -y --upgrade pip setuptools wheel && pip3 install -y Adafruit_DHT
WORKDIR /app
CMD ["python3", "terrarium_monitor.py"]
#&& pip install --force-pi adafruit-circuitpython-dht
#apt-get install -Y build-essential && apt-get install -Y python-dev && pip3 install Adafruit_Python_DHT

