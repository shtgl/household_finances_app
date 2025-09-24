from flask import Flask

from configs import DefaultConfig
from routes.schema import (create_schema,
                    User, 
                    db, mail, login_manager, bcrypt)
from logger.log_utility import setup_logger


CONFIG = DefaultConfig()
base_logger = setup_logger()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():
    """
    Main app function
    """
    app = Flask(__name__)
    base_logger.info(f"Creating app")
    app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG.SQLALCHEMY_DB
    app.config['SECRET_KEY'] = CONFIG.SECRET_KEY
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = CONFIG.SQLALCHEMY_TM

    # Init extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    
    app.config['MAIL_SERVER'] = CONFIG.MAIL_SERVER
    app.config['MAIL_PORT'] = CONFIG.MAIL_PORT
    app.config['MAIL_USE_TLS'] = CONFIG.MAIL_USE_TLS
    app.config['MAIL_USE_SSL'] = CONFIG.MAIL_USE_SSL
    app.config['MAIL_USERNAME'] = CONFIG.MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = CONFIG.MAIL_PASSWORD


    mail.init_app(app)
    
    # Register blueprints
    from routes import auth, dashboard
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)

    with app.app_context():
        create_schema(app)

    return app

    
if __name__ == "__main__":
    app = create_app()
    
    app.run(debug=True)