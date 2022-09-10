#!/usr/bin/env/ python
# -*- coding: utf8 -*-
"""
Classe principal, executa e faz a interfase de comunicação com a aplicação frontend.
"""
#import board
import os
import datetime
import sys
import json # used to parse config.json
import time # timer functions
from RPi import GPIO
from gpiozero import LightSensor
import Adafruit_DHT

# from adafruit_dht import DHT11
# import board

import paho.mqtt.client as mqtt
sys.path.append(r'/home/brunohp/Documentos/development/terrariumtarget/src')
import atomic_terrarium as AT

GPIO.setwarnings(False)

gpio_irriga = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_irriga,  GPIO.OUT)
GPIO.output(gpio_irriga, GPIO.LOW)

gpio_lumi = 4
gpio_umi  = 22
gpio_temp_umi = 27


        #MQTT Details
broker_address="broker.emqx.io"   #"iot.eclipse.org"
client_id="raspberry"
PortaBroker = 1883
KeepAliveBroker = 60


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


#MQTT init
print("Initalizing MQTT Client instance: " + client_id)
client =  mqtt.Client(client_id) #define de topic "raspiberry"
#Connect to broker
print("connecting to broker: " + broker_address)
client.connect(broker_address)



def read_tem_umi(gpio):
    """
    Leitura e tratamendo dos dados do sensor de temperatura e umidade
    """
    temperature = 0
    humidity = 0
    try:

        DHT_SENSOR = Adafruit_DHT.DHT11
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, gpio)
#
#         dht_device = DHT11(board.D27, use_pulseio=False)
#         temperature = dht_device.temperature
#         humidity = dht_device.humidity  
        

        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*  Humidity{1:0.1f}%'.format(temperature,humidity))
            return temperature, humidity
        else:
            print('Failed to get reading. Try again!')
    except Exception as e: 
        print(repr(e))
        return temperature, humidity
        #caso ocorrra algum erro entra em excecao
        #print "ERR_RANGE"
        print("ISSUE IN READING DHT11")
        #exit(0) 

    time.sleep(5)



def percebe_luz(gpio):
    sensor = LightSensor(gpio) 
    
    if sensor.value > 0.0:
        return 0
    return 1

def percebe_umidade(gpio):
    sensor = LightSensor(gpio) 
    
    if sensor.value > 0.0:
        return 0
    return 1


#Callback function on message receive
def on_message(message): #client,userdata,
    """
    sobrescreve a função a ser enviada que formata a mensagem a ser enviada
    """
    print("message received",str(message.payload.decode("utf-8")))
    data = json.loads(str(message.payload.decode("utf-8","ignore")))
    #print(data)
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=", message.retain)
    return data


        #callback function on log
def on_log(buf): #client, userdata, level,
    """
    leitura das informações no buffer de chegada e saida de dados.
    """
    print("log: ", buf)

def publish(client):
    """
    publica dados coletados no cliente MQTT.
    """
    global gpio_umi, gpio_lumi, gpio_temp_umi, gpio_irriga
    pub_topic_temp="greenhouse/temp"
    pub_topic_umi="greenhouse/umi"
    pub_topic_umi_ar="greenhouse/umi_ar"
    pub_topic_lumi="greenhouse/lumi"

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print ("checking temperatura and posting")
    #temperatura
    tmp_umi = read_tem_umi(gpio_temp_umi)
    if tmp_umi is not None:
        data = AT.form_data(timestamp,tmp_umi[0],pub_topic_temp)
        #punblish to topic
    client.publish(pub_topic_temp, data)
    print ("\nchecking umidade do ar and posting")
        #Umidade Ar
    if tmp_umi is not None:
        data = AT.form_data(timestamp,tmp_umi[1],pub_topic_temp)
        #punblish to topic
    client.publish(pub_topic_umi_ar, data)
    #Umidade
    print ("\nchecking umidde and posting")
    data = AT.form_data(timestamp,percebe_umidade(gpio_umi),pub_topic_umi)
    #punblish to topic
    client.publish(pub_topic_umi, data)
    #luminosidade
    print ("\nchecking luminosidade and posting")
    data = AT.form_data(timestamp,percebe_luz(gpio_lumi),pub_topic_lumi)
    #punblish to topic
    client.publish(pub_topic_lumi, data)

    print("Sleeping\n\n")
    time.sleep(5)

    client.on_log = on_log

def run_monitor() :
    """
    Principal função, executa funções da aplicação backend.
    """
    global sub_topic
    try:
        while True:
            #print("subscribing to topic on client" + sub_topic)
            #client.subscribe(sub_topic)
            publish(client)
            client.on_message = on_message
            mensage = client.subscribe("topic/react")
            print("retorno mensage ",client.subscribe("topic/react"))
            
            print("retorno mensage ",mensage)
            if AT.aciona_irrigacao(on_message):
                GPIO.output(gpio_irriga, GPIO.HIGH)
                time.sleep(5)
                GPIO.output(gpio_irriga, GPIO.LOW)


    except Exception as e:
        client.loop_stop()
        print(e)

if __name__ == '__main__':
    """
    Roda funcionalidades do modulo.
    """
    run_monitor()
