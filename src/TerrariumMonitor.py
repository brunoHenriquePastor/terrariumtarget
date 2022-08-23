#!/usr/bin/env/ python
# -*- coding: utf8 -*-
import paho.mqtt.client as mqtt
import os
import datetime
import sys
sys.path.append(r'/home/brunohp/Documentos/development/terrariumtarget/src')
import json # used to parse config.json
import time # timer functions
import RPi.GPIO as GPIO
import TCC.terrariumtarget.src.atomic_terrarium as AT

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.IN)
GPIO.setup(3, GPIO.IN)
GPIO.setup(4, GPIO.IN)

GPIO.setup(5, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)

sensor_umi  = 2
sensor_lumi0 = 3
sensor_lumi1 = 5
sensor_temp_umi = 4

GPIO.input(sensor_umi)
GPIO.input(sensor_lumi0)
GPIO.input(sensor_lumi0)
GPIO.input(sensor_temp_umi)


# sensor_umi  = GPIO.input(2)
# sensor_lumi = GPIO.input(3)
# sensor_temp = GPIO.input(4)

        # VARIAVEL PARA ARMAZENAR A LEITURA
varUmi  = 0.0
varLumi = 0.0
varTemp = 0.0

        # VARIAVEL PARA MARCAR A VEZ DE QUAL PORTA SERÁ LIDA
leitura = 0

        #MQTT Details
broker_address="broker.emqx.io"   #"iot.eclipse.org"
client_id="raspberry"
pub_topic_temp="greenhouse/temp"
pub_topic_umi="greenhouse/umi"
pub_topic_umi_ar="greenhouse/umi_ar"
pub_topic_lumi="greenhouse/lumi"
sub_topic="greenhouse/temp"
PortaBroker = 1883
KeepAliveBroker = 60


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# base_dir = '/sys/bus/w1/devices/'
 # device_file_list = glob.glob(base_dir + '28*')[0] + '/w1_slave'



#class Terrarium:
      
#MQTT init
print("Initalizing MQTT Client instance: " + client_id)
client =  mqtt.Client(client_id) #define de topic "raspiberry"
#Connect to broker
print("connecting to broker: " + broker_address)
client.connect(broker_address)

def bin2dec(string_num):
    return str(int(string_num, 2))


def read_tem_umi(sensor):
    data = []

    if len(data) > 0 :
        #remove os itens do array que recupera os dados
        del data[0: len(data)]
                            
                    
    #armazena os dados lidos do pino 4 na variavel global data
    for i in range(0, 500):
        data.append(GPIO.input(sensor))
        #declara as variaveis que irao receber os bits lidos
    bit_count = 0
    tmp = 0
    count = 0
    HumidityBit = ""
    TemperatureBit = ""
    crc = ""
                    
    #inicia a tentativa de recuperar os bits 
    try:
        while data[count] == 1:
            tmp = 1
            count = count + 1
                    
        for i in range(0, 32):
            bit_count = 0
                    
            while data[count] == 0:
                tmp = 1
                count = count + 1
            while data[count] == 1:
                bit_count = bit_count + 1
                count = count + 1
                    
            if bit_count > 3:
                if i>=0 and i<8:
                    HumidityBit = HumidityBit + "1"
                if i>=16 and i<24:
                    TemperatureBit = TemperatureBit + "1"
            else:
                if i>=0 and i<8:

                    HumidityBit = HumidityBit + "0"
                if i>=16 and i<24:
                    TemperatureBit = TemperatureBit + "0"
                    
    except:
        #caso ocorrra algum erro entra em excecao
        #print "ERR_RANGE"
        print("ERRO NA RESPOSTAS DE BITS")
        #exit(0)
                    
                    
    #tenta fazer verificacao se os bits forao recebidos corretamente (total sao 8)
    try:
        for i in range(0, 8):
            bit_count = 0
            
            while data[count] == 0:
                tmp = 1
                count = count + 1
            
            while data[count] == 1:
                bit_count = bit_count + 1
                count = count + 1
        
        if bit_count > 3:
            crc = crc + "1"
        else:
            crc = crc + "0"
                                    
    except:
        #print "ERR_RANGE"
        print("ERRO NA RESPOSTAS DE BITS")
        #exit(0)
                    
                    
        #E por fim Tenta fazer a conversao de binario para inteiro
        # chamando o metodo bin2dec e armazena nas variaveis
        # HUmidity e  Temperature
    try:
        Humidity = bin2dec(HumidityBit)
        Temperature = bin2dec(TemperatureBit)
                    
        if int(Humidity) + int(Temperature) - int(bin2dec(crc)) == 0:
            return Temperature, Humidity
                    
    except:
        print("ERRO DE CONVERSAO DE BINARIO PARA INTEIRO")
        #exit(0)
                    
    time.sleep(10)



def descarga():
    GPIO.setup(sensor_lumi0,GPIO.IN)
    GPIO.setup(sensor_lumi1,GPIO.OUT)
    GPIO.output(sensor_lumi1,0)
    time.sleep(0.005)

def carga():
    GPIO.setup(sensor_lumi1,GPIO.IN)
    GPIO.setup(sensor_lumi0,GPIO.OUT)
    contador = 0
    GPIO.output(sensor_lumi0,1)
    while(GPIO.input(sensor_lumi1)==0):
        contador = contador + 1
    time.sleep(3)
    return contador



def leitura_analogica():
    descarga()
    return carga()

def inten_lum():
    if leitura_analogica() > 100:
        return 1
    return 0



#Callback function on message receive
def on_message(client,userdata,message):
    print("message received",str(message.payload.decode("utf-8")))
    data = json.loads(str(message.payload.decode("utf-8","ignore")))
    print(data)
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=", message.retain)
    return data


        #callback function on log
def on_log(client, userdata, level,buf):
    print("log: ", buf)

def publish(client):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print ("checking temp and posting")
    #temperatura
    data = AT.form_data(timestamp,read_tem_umi(sensor_temp_umi)[0],pub_topic_temp)
    #punblish to topic
    client.publish(pub_topic_temp, data)
    print ("checking umi ar and posting")
    #Umidade Ar
    data = AT.form_data(timestamp, read_tem_umi(sensor_temp_umi)[1], pub_topic_temp)
        #punblish to topic
    client.publish(pub_topic_umi_ar, data)
    #Umidade
    print ("checking umi and posting")
    data = AT.form_data(timestamp,GPIO.input(sensor_umi),pub_topic_umi)
    #punblish to topic
    client.publish(pub_topic_umi, data)
    #luminosidade
    print ("checking luminosidade and posting")
    data = AT.form_data(timestamp,inten_lum(),pub_topic_lumi)
    #punblish to topic
    client.publish(pub_topic_lumi, data)

    print("Sleeping")
    time.sleep(1)

    client.on_log = on_log

try:    
    while True:
        print("subscribing to topic " + sub_topic)
        client.subscribe(sub_topic)
        result = publish(client)
        client.subscribe('testtopic/react')
        client.on_message = on_message
        if (AT.aciona_irrigacao(on_message)):
            GPIO.output(17, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(17, GPIO.LOW)
                        
                        

except Exception as e:
    client.loop_stop()
    print(e)


