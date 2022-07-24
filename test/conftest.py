from venv import create
import sys 
sys.path.append(r'/home/brunohp/Documentos/development/terrariumtarget')
import pytest
import src.TerrariumMonitor

@pytest.fixture(scope="module")
def TerrariumMonitor():
    """Instance of monitor aplication"""
    return src.TerrariumMonitor.create_TerrariumMonitor()