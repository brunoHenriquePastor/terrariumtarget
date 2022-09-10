FROM arm64v8/python
COPY /src /app
RUN apt-get -qq update && python -m pip install --upgrade pip && apt-get --allow install python3-pip && pip --allow install paho-mqtt && pip --allow install RPi.GPIO
RUN python3 -m pip --allow install --upgrade pip setuptools wheel && pip3 --allow install Adafruit_DHT
WORKDIR /app
CMD ["python3", "terrarium_monitor.py"]

#&& pip install --force-pi adafruit-circuitpython-dht
#apt-get install -Y build-essential && apt-get install -Y python-dev && pip3 install Adafruit_Python_DHT

