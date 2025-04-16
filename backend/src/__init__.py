import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from src.config import Config
from src.middlewares.agent_check import restrict_user_agents

# Init db
db = SQLAlchemy()

def create_app():
    
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(message)s")
    
    # Load env variables
    load_dotenv(override=True)

    # Create app
    app = Flask(__name__)

    # Handling CORS
    CORS(app)
    app.config.from_object('src.config.Config')

    # Middlewares
    # Agent check
    # restrict_user_agents(app)

    # Configuration
    try:
        app.config.from_object(Config)
        logging.info("Configuration Success")
    except Exception as e:
        logging.error("Configuration Failed")

    # Connect the db to app
    try:
        db.init_app(app)
        logging.info("DB Initialized Successfully.")
    except Exception as e:
        logging.error("DB Initialize Failed")

    jwt = JWTManager(app)

    # Init migration
    migrate = Migrate(app, db)
    logging.info("Migrate Initialized Successfully.")

    # Import routes
    try:
        from src.routes import init_routes
        init_routes(app)
        logging.info("Routes Initialized Successfully.")
    except Exception as e:
        logging.error("Routes Initialize Failed")

    # with app.app_context():
    #     db.create_all()

    return app
