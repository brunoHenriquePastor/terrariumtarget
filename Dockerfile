FROM arm64v8/python
COPY /src /app
RUN apt-get -qq update && python -m pip install --upgrade pip && apt-get --yes --force-yes install python3-pip && pip --yes --force-yes install paho-mqtt && pip --yes --force-yes install RPi.GPIO
RUN python3 -m pip --yes --force-yes install --upgrade pip setuptools wheel && pip3 --yes --force-yes install Adafruit_DHT
WORKDIR /app
CMD ["python3", "terrarium_monitor.py"]
#&& pip install --force-pi adafruit-circuitpython-dht
#apt-get install -Y build-essential && apt-get install -Y python-dev && pip3 install Adafruit_Python_DHT

