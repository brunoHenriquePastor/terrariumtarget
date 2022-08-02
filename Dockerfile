FROM arm32v7/python:3
COPY /src /app
RUN apt-get -qq update && install python3 && python -m pip install --upgrade pip && pip install paho-mqtt
WORKDIR /app
CMD ["python3", "TerrariumMonitor.py"]
# install python3 &&