FROM arm64v8/python
COPY /src /app
RUN apt-get -qq update && python -m pip install --upgrade pip && pip install paho-mqtt && pip install RPi.GPIO
WORKDIR /app
CMD ["python3", "TerrariumMonitor.py"]
# install python3 &&v