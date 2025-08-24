from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    
    db.init_app(app)

    login_manager.init_app(app)

    csrf.init_app(app)

    from app.routes import main as main

    app.register_blueprint(main)
    login_manager.login_view = 'main.login'  
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"
    
    return app
