import logging
from flask import Flask, render_template, redirect
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
    print(os.getenv('DATABASE_URL'))
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    swagger = Swagger(app)

    with app.app_context():
        db.engine.connect()
        print('Connected to the database')
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

    with app.app_context():
        from app.routes import artist_routes, team_routes, gallery_routes
        app.register_blueprint(artist_routes.bp, url_prefix='/artists')
        app.register_blueprint(team_routes.bp, url_prefix='/teams')
        app.register_blueprint(gallery_routes.bp, url_prefix='/galleries')

    return app

app = create_app()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def redirect_to_artists():
    return redirect('/artists')

if __name__ == '__main__':
    app.run(debug=True)