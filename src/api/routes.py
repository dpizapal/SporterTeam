"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Evento
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import cloudinary
import cloudinary.uploader

api = Blueprint('api', __name__)

# ENDPOINT REGISTRO DE USUARIO NUEVO Y CHECK SI EXISTE


@api.route("/register", methods=["POST"])
def create_user():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    age = request.json.get("age")
    user = User(email=email, password=password, username=username, age=age)
    user_email = User.query.filter_by(email=email).one_or_none()
    user_username = User.query.filter_by(username=username).one_or_none()
    if user_email or user_username:
        return jsonify({"msg": "El usuario ya existe"}), 401
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "user register"}), 200


# ENDPOINT PARA CAMBIAR DATOS DEL PERFIL DEL USUARIO

@api.route("/edituser", methods=["POST"])
@jwt_required()
def edit_user():
    new_username = request.json.get("new_username")
    new_email = request.json.get("new_email")
    new_password = request.json.get("new_password")
    new_age = request.json.get("new_age")
    new_description = request.json.get("new_description")
    current_user = User.query.filter_by(email=get_jwt_identity()).first()

    user_new_email = User.query.filter_by(email=new_email).one_or_none()
    user_new_username = User.query.filter_by(
        username=new_username).one_or_none()
    if user_new_username or user_new_email:
        return jsonify({"msg": "username o email ya existen"}), 401
    if new_username:
        current_user.username = new_username
    if new_email:
        current_user.email = new_email
    if new_password:
        current_user.password = new_password
    if new_age:
        current_user.age = new_age
    if new_description:
        current_user.description = new_description

    db.session.commit()

    return jsonify({"msg": "Perfil actualizado"}), 200


# ENDPOINT PARA OBTENER EL TOKEN EN EL LOGIN
@api.route('/token', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"msg": "El usuario no existe"}), 401
    elif email != user.email or password != user.password:
        return jsonify({"msg": "La contraseña o usuario es incorrecto o no existe"}), 402

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

# CARGAR IMAGEN EN LA BASE DE DATOS


@api.route('/upload', methods=['POST'])
@jwt_required()
def handle_upload():
    identity = get_jwt_identity()  # pide el token
    user1 = User.query.filter_by(email=identity).one_or_none()
    result = cloudinary.uploader.upload(request.files['profile_image'])
    user1.profile_image_url = result['secure_url']
    db.session.add(user1)
    db.session.commit()

    return jsonify(user1.profile_image_url), 200
    # return jsonify(user1.profile_image_url), 200


@api.route('/upload', methods=['DELETE'])
@jwt_required()
def handle_deleteimage():
    identity = get_jwt_identity()  # pide el token
    user1 = User.query.filter_by(email=identity).one_or_none()
    user1.profile_image_url = "https://img.freepik.com/vector-premium/perfil-hombre-dibujos-animados_18591-58482.jpg?w=200"
    db.session.commit()

    return jsonify(user1.profile_image_url), 200
    # return jsonify(user1.profile_image_url), 200

# ENDPOINT PARA TRAER LA IMAGEN DE PERFIL DE LA BASE DE DATOS


@api.route('/load', methods=['GET'])
@jwt_required()
def handle_load():
    identity = get_jwt_identity()
    user = User.query.filter_by(email=identity).one_or_none()

    return jsonify(user.profile_image_url), 200
# ENDPOINT PARA OPTENER TODOS LOS EVENTOS


@api.route('/eventos', methods=["GET"])
def get_eventos():
    try:
        response = [x.serialize() for x in Evento.query.all()]
        return jsonify(response), 200
    except:
        return jsonify("invalid Method "), 401
# endpoint para apuntarse a un evento


@api.route('/joinevent', methods=["POST"])
@jwt_required()
def post_eventos():
    eventId = request.json.get("id")
    identity = get_jwt_identity()
    user = User.query.filter_by(email=identity).one_or_none()
    event = Evento.query.filter_by(id=eventId).one_or_none()

    user.participant.append(event)
    db.session.commit()

    return jsonify("participant add"), 200


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200
