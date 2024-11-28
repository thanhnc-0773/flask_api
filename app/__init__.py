import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flasgger import Swagger
import os

# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    swagger = Swagger(app)

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

    with app.app_context():
        from app.routes import artist_routes, team_routes
        app.register_blueprint(artist_routes.bp, url_prefix='/artist')
        app.register_blueprint(team_routes.bp, url_prefix='/team')

        # Register error handlers
        from app.errors import errors
        app.register_blueprint(errors)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)