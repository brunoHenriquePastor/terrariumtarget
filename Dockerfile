FROM arm64v8/python
COPY /src /app
RUN apt-get -qq update && python -m pip install --upgrade pip && pip install paho-mqtt && pip install RPi.GPIO && pigpiod
RUN sudo apt-get install build-essential && sudo apt-get install python-dev && pip3 install Adafruit_Python_DHT
WORKDIR /app
CMD ["python3", "terrarium_monitor.py"]
#&& pip install --force-pi adafruit-circuitpython-dht