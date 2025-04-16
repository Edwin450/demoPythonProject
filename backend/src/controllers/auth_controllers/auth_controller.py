import datetime
import bcrypt
from src import db
from flask import jsonify, request
from src.models.auth_models.user_model import User
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)


def register_controller():

    try:

        data = request.get_json()

        username = data.get("username")
        password = data.get("password")
        role = data.get("role", "user")

        if User.query.filter_by(username=username).first():
            return jsonify({"msg": "User already exists", "success": 2})

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        new_user = User(
            username=username, password=hashed_password.decode("utf-8"), role=role
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "User registered successfully", "status": 1}), 201

    except Exception as e:
        db.session.rollback()
        return (jsonify({"success": 0, "error": str(e)}), 500)


def login_controller():

    try:

        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return (
                jsonify({"message": "Username and password required", "status": 0}),
                400,
            )

        user = User.query.filter_by(username=username).first()

        if not user or not bcrypt.checkpw(
            password.encode("utf-8"), user.password.encode("utf-8")
        ):
            return jsonify({"message": "Invalid credentials", "status": 0})

        additional_claims = {
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
        }

        # Generate JWT token
        access_token, refresh_token = generate_tokens(identity=user.id)

        user.refresh_token = refresh_token
        user.refresh_token_created_at = datetime.datetime.utcnow()
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "username": user.username,
                    "role": user.role,
                    "status": 1,
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return (jsonify({"success": 0, "error": str(e)}), 500)


def token_refresh_controller():

    try:

        refresh_token = request.headers.get("Authorization")
        if not refresh_token or not refresh_token.startswith("Bearer "):
            return (
                jsonify({"message": "Refresh token missing or invalid", "status": 0}),
                400,
            )

        refresh_token = refresh_token.split(" ")[1]

        identity = get_jwt_identity()

        user = User.query.filter_by(id=identity).first()
        if not user:
            return jsonify({"message": "User not found", "status": 0}), 404

        if refresh_token != user.refresh_token:
            return jsonify({"message": "Invalid refresh token", "status": 0}), 401

        access_token, new_refresh_token = generate_tokens(identity)
        user.refresh_token = new_refresh_token
        user.token_created_at = datetime.datetime.utcnow()
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Access token refreshed",
                    "access_token": access_token,
                    "refresh_token": new_refresh_token,
                    "status": 1,
                }
            ),
            200,
        )
    except Exception as e:
        return (jsonify({"success": 0, "error": str(e)}), 500)

def generate_tokens(identity, additional_claims=None, expires_delta=None):
    access_token = create_access_token(
        identity=identity,
        additional_claims=additional_claims,
        expires_delta=datetime.timedelta(seconds=30),
    )

    refresh_token = create_refresh_token(
        identity=identity, expires_delta=datetime.timedelta(minutes=2)
    )

    return access_token, refresh_token
