from flask import Flask
from config import Config
from .routes import main_bp

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.secret_key = Config.SECRET_KEY
    app.config.from_object('config.Config')

    # Register blueprint untuk routes
    app.register_blueprint(main_bp)

    return app
