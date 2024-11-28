from flask import Flask
from app.extensions import db, migrate
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from flask_login import LoginManager
from app.chatbot import chatbot_bp



# Initialize extensions
# db = SQLAlchemy()
# migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login'  # Default login route
login_manager.login_message = "Please log in to access this page."

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'uchechukwu'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lessons.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Bind extensions to the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register Blueprints
    from app.main.routes import main as main_blueprint
    from app.admin.routes import admin as admin_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    # app.register_blueprint(chatbot_bp, url_prefix='/api')
    app.register_blueprint(chatbot_bp)
    return app

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
