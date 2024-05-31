from flask_session import Session

def init_app(app):
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)