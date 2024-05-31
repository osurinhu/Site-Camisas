from importlib import import_module
from dynaconf import FlaskDynaconf

def carregar_extensoes(app):
    for extensao in app.config.get("EXTENSOES"):
       modulo = import_module(extensao)
       modulo.init_app(app) 


def init_app(app):
    FlaskDynaconf(app)