"""
Funções responsáveis por realizar ações de comando externo. Passam pelo teste estatico com o doctest.
"""

import json

def form_data(times, sensor, pub_topic):
        list = [times, str(sensor)]
        data = json.dumps(list)
        print("Publish to Topic" + pub_topic)
        print (str(sensor))
        return data

def aciona_irrigacao(data):
        if data == "AAA" :
                return True
        return False
