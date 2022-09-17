FROM arm64v8/python

COPY /src /app

RUN apt install python3 && \
    python3 -m venv tutorial-env && \
    pip3 install pip &&  pip3 install \
    setuptools \
    paho-mqtt \
    gpiozero \
    RPi.GPIO \
    board \
    Adafruit-Blinka

RUN python3 -m pip install --upgrade pip setuptools wheel && pip3 install \
    --install-option="--force-pi" Adafruit_DHT \
    adafruit-circuitpython-dht 
    #adafruit-python-shell
 

WORKDIR /app

CMD ["python3", "terrarium_monitor.py"]
