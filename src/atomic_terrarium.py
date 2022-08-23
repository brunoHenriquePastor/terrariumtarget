"""
Modulo responsavel por realizar ações de comando externo.
Passam pelo teste estatico com o doctest.
"""

import json

def form_data(times, sensor, pub_topic):
    """
    Função que trata a formatação dos dados a serem enviados
    """
    lista = [times, str(sensor)]
    data = json.dumps(lista)
    print("Publish to Topic" + pub_topic)
    print (str(sensor))
    return data

def aciona_irrigacao(data):
    """
    Função que executa o processo de atuação do sistema de irrigação pelo comando remoto.
    """
    if data == "AAA" :
        return True
    return False
