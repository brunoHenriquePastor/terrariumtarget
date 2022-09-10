FROM arm64v8/python
COPY /src /app
RUN apt install python3 && pip install pip && pip install paho-mqtt && pip3 install gpiozero
RUN python3 -m pip install --upgrade pip setuptools wheel && pip3 install RPI.GPIO && pip3 install --install-option="--force-pi" Adafruit_DHT
WORKDIR /app
CMD ["python3", "terrarium_monitor.py"]

# apt -qq update &&
#&& pip install --force-pi adafruit-circuitpython-dht 
#apt-get install -Y build-essential && apt-get install -Y python-dev && pip3 install Adafruit_Python_DHT
#&& python -m pip install --upgrade pip

#apt install python3-dev python3-pip && python3 -m pip install --upgrade pip setuptools wheel && pip3 --force-pi install Adafruit_DHT #maybe i just need do learne the right way for spacify force pi

#pip3 install adafruit-blinka
