FROM arm64v8/python

COPY /src /app

RUN apt install python3 && \
    pip3 install pip && \
    python3 -m venv tutorial-env && \
    pip3 install paho-mqtt && \
    pip3 install gpiozero && pip3 install libgpiod2 && \
    pip3 install board

RUN python3 -m pip install --upgrade pip setuptools wheel && \
    pip3 install --upgrade adafruit-python-shell && \
    pip3 install RPi.GPIO && \
    pip3 install --install-option="--force-pi" Adafruit_DHT==1.4.0 && \
    pip install adafruit-circuitpython-dht && \
    pip3 install adafruit-circuitpython-busdevice
    # pip install CircuitPython && \
    # pip install Blinka

# RUN pip3 install gpiod && \
#     pip3 install libgpiod-dev git build-essential && \
#     git clone https://github.com/adafruit/libgpiod_pulsein.git && \
#     cd libgpiod_pulsein/src && \ 
#     make && \
#     cp libgpiod_pulsein /usr/local/lib/python3.8/dist-packages/adafruit_blinka/microcontroller/bcm283x/pulseio/libgpiod_pulsein
# RUN git clone https://github.com/adafruit/Adafruit_Python_DHT.git && \
# 	cd Adafruit_Python_DHT && \
# 	python3 setup.py install --force-pi

WORKDIR /app

CMD ["python3", "terrarium_monitor.py"]


#RUN mkdir /home/anholt/rpi2/debugfs && git clone https://github.com/raspberrypi/firmware raspberrypi-firmware && cp -R raspberrypi-firmware/boot/ /home/anholt/rpi2/


#RUN wget --no-check-certificate https://www.meinbergglobal.com/download/drivers/mbgtools-lx-4.2.6.tar.gz && tar xvzf mbgtools-lx-4.2.6.tar.gz && cd mbgtools-lx-4.2.6
# RUN git clone https://github.com/adafruit/Adafruit_Python_DHT.git && \
# 	cd Adafruit_Python_DHT && \
# 	python3 setup.py install --install-option="--force-pi"

#pip3 install adafruit-blinka
#pip install Adafruit-DHT

 #apt install build-essential python-dev


 #pip3 install libgpiod-dev git build-essential && \