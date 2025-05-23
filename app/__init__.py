from flask import Flask
from .database import init_db

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object('config.Config')

    # Inisialisasi database
    init_db(app)

    # Register blueprint untuk routes
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
