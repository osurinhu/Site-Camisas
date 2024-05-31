from flask import Flask
from Site_Camisas.extensoes import configuracao

#BLUEPRINTS
from Site_Camisas.blueprints.autenticacao.autenticacao import autenticacao_bp

def create_app():
    app = Flask(__name__)
    configuracao.init_app(app) #Carregar configs
    configuracao.carregar_extensoes(app) #Carregar extensoes
    
    # Carregar Blueprints
    app.register_blueprint(autenticacao_bp)

    return app
