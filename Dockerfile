FROM arm64v8/python
COPY /src /app
RUN apt install python3 && pip install pip && pip install paho-mqtt && pip3 install gpiozero && pip install board
RUN python3 -m pip install --upgrade pip setuptools wheel && pip3 install RPI.GPIO && pip3 install --install-option="--force-pi" Adafruit_DHT 
RUN pip3 install adafruit-circuitpython-dht
WORKDIR /app
CMD ["python3", "terrarium_monitor.py"]

#pip3 install adafruit-blinka
