from flask import Flask
from Site_Camisas.extensoes import configuracao

#BLUEPRINTS
from Site_Camisas.blueprints.autenticacao.views import autenticacao_bp
from Site_Camisas.blueprints.admin.views import admin_bp
from Site_Camisas.blueprints.cartfav.views import cartfav_bp
from Site_Camisas.blueprints.produto.views import produto_bp

def create_app():
    app = Flask(__name__)
    configuracao.init_app(app) #Carregar configs
    configuracao.carregar_extensoes(app) #Carregar extensoes
    
    # Carregar Blueprints
    app.register_blueprint(autenticacao_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(cartfav_bp)
    app.register_blueprint(produto_bp)

    return app
