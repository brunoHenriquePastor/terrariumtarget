FROM arm64v8/python
COPY /src /app
RUN apt-get -qq update && python -m pip install --upgrade pip && pip install paho-mqtt && pip install RPi.GPIO && sudo adduser pi gpio
WORKDIR /app
CMD ["python3", "terrarium_monitor.py"]
# install python3 && "sudo"