from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from services.database import db


app = create_app()

with app.app_context():
  db.init_app(app)
  db.create_all()

# @app.route("/")
# def ping():
#   return "pong!!"



# @app.route("/hello")
# def say_hello():
#   return jsonify({"message":"Hola mundo"})


if(__name__) == '__main__':
    app.run(debug=True, port=5000)