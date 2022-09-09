FROM arm64v8/python
COPY /src /app
RUN apt-get -qq update && python -m pip install --upgrade pip && apt-get install python3-pip && pip install paho-mqtt && pip install RPi.GPIO
RUN python3 -m pip install -Y --upgrade pip setuptools wheel && pip3 install -Y Adafruit_DHT
WORKDIR /app
CMD ["python3", "terrarium_monitor.py"]
#&& pip install --force-pi adafruit-circuitpython-dht
#apt-get install -Y build-essential && apt-get install -Y python-dev && pip3 install Adafruit_Python_DHT

