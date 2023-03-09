from flask import Flask, jsonify
from dotenv import load_dotenv
import os
from services.database import db
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from constants.swagger import swagger_config, template
from constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

load_dotenv()


def create_app(test_config = None):
  
  app = Flask(__name__, instance_relative_config=True)

  if test_config is None:
    app.config.from_mapping(
      SECRET_KEY = os.environ["SECRET_KEY"],
      SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"],
      SQLALCHEMY_TRACK_MODIFICATIONS = False,
      JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"],
      SWAGGER = {
        'title': "Bookmarks API",
        "uiversion" : 3
      }
    )
    

  else:
    app.config.from_mapping(test_config)


  db.app = app
  
  JWTManager(app)


  from routes.auth import auth
  
  app.register_blueprint(auth)
  from routes.bookmarks import bookmarks
  
  app.register_blueprint(bookmarks)
  
  Swagger(app, template = template, config =swagger_config)

  @app.errorhandler(HTTP_404_NOT_FOUND)
  def handle_404(e):
      return jsonify({'error': 'Not found'}), HTTP_404_NOT_FOUND

  @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
  def handle_500(e):
      return jsonify({'error': 'Something went wrong, we are working on it'}), HTTP_500_INTERNAL_SERVER_ERROR

  return app



