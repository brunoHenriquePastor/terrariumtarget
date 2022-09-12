FROM arm64v8/python
COPY /src /app
RUN apt install python3 && pip install pip && pip install paho-mqtt && pip3 install gpiozero && pip install board
RUN python3 -m pip install --upgrade pip setuptools wheel && pip3 install --upgrade adafruit-python-shell && pip3 install RPI.GPIO && pip3 install --install-option="--force-pi" Adafruit_DHT==1.4.0  
#RUN apt-get install -y python3 python3-dev python3-venv python3-pip bluez libffi-dev libssl-dev libjpeg-dev zlib1g-dev autoconf build-essential libopenjp2-7 libtiff5 libturbojpeg0-dev tzdata
RUN --name homeassistant \
  --privileged \
  --restart=unless-stopped \
  -e TZ=MY_TIME_ZONE \
  -v /PATH_TO_YOUR_CONFIG:/config \
  --network=host \
  ghcr.io/home-assistant/home-assistant:stable
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