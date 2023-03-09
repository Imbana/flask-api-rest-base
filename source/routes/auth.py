from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash
from constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_200_OK, HTTP_401_UNAUTHORIZED
from models.user import User
from services.database import db
import validators
from flasgger import swag_from

auth = Blueprint("auth",__name__, url_prefix="/api/v1/auth")


@auth.route("/register", methods=("POST",))
@swag_from("../constants/docs/register.yaml")
def register():
  username = request.json.get('username', "")
  email = request.json.get('email', "")
  password = request.json.get('password',"")
  # password = request.json['password']

  if len(password) < 6:
      return jsonify({'error': "Password is too short"}), HTTP_400_BAD_REQUEST

  if len(username) < 3:
      return jsonify({'error': "User is too short"}), HTTP_400_BAD_REQUEST

  if not username.isalnum() or " " in username:
      return jsonify({'error': "Username should be alphanumeric, also no spaces"}), HTTP_400_BAD_REQUEST

  if not validators.email(email):
      return jsonify({'error': "Email is not valid"}), HTTP_400_BAD_REQUEST

  if User.query.filter_by(email=email).first() is not None:
      return jsonify({'error': "Email is taken"}), HTTP_409_CONFLICT

  if User.query.filter_by(username=username).first() is not None:
      return jsonify({'error': "username is taken"}), HTTP_409_CONFLICT

  pwd_hash = generate_password_hash(password)

  user = User(username=username, password=pwd_hash, email=email)
  db.session.add(user)
  db.session.commit()

  return jsonify({
      'message': "User created",
      'user': {
          'username': username, "email": email
      }

  }), HTTP_201_CREATED

@auth.route("/login", methods=("POST",))
@swag_from("../constants/docs/login.yaml")
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    user = User.query.filter_by(email=email).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify({
                'user': {
                    'refresh': refresh,
                    'access': access,
                    'username': user.username,
                    'email': user.email
                }

            }), HTTP_200_OK

    return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED
  
  
@auth.route("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        'username': user.username,
        'email': user.email
    }), HTTP_200_OK


@auth.route('/token/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        'access': access
    }), HTTP_200_OK