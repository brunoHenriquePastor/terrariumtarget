"""
Modulo que define as funções que passam por testes estáticos no Doctest.
"""

import random
from datetime import date
import sys
import doctest
import uuid
sys.path.append(r'/home/brunohp/Documentos/development/terrariumtarget/src')
import src.atomic_terrarium as AT


aleatorio = 10*random.random()
SAlea = uuid.uuid4()

def test_form_data():
    """
    Teste da função que gera o formado do dado a ser enviado.
    """
    Sdate = str(date(2000, 1, 4))
    Svalor = str(aleatorio)
    '''
    >>> test_form_data()
    str([Sdate,Svalor])
    '''
    data = AT.form_data(str(date(2000, 1, 4)), aleatorio, "greenhouse/temp")
    print(data)

    return data

def test_aciona_irrigacao(data):
    '''
    >>> test_aciona_irrigacao("AAA")
    True
    >>> test_aciona_irrigacao(SAlea)
    False
    '''
    return AT.aciona_irrigacao(data)

# def test_test_request_returns_200():
#      client.get("broker.emqx.io").status_code

if __name__ == '__main__':
    """
    Roda funcionalidades do modulo.
    """
    doctest.testmod()