import os
import uuid
from helpers.uuid import is_valid_uuid
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# postgres
url = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User Model


class Users(db.Model):
    # __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    email = db.Column(db.String)
    genre = db.Column(db.String)

    def __repr__(self):
        return f'<User {self.name}: email - {self.email}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'genre': self.genre
        }


# before first


@app.route("/")
def home():
    return jsonify({"message": "Fuck you!"})


@app.route("/users", methods=['GET'])
def get_users():
    users = Users.query.all()
    return jsonify([user.to_dict() for user in users])


@app.route("/users/<user_id>", methods=['GET'])
def get_user(user_id):

    if not is_valid_uuid(user_id):
        return jsonify({"message": "Invalid UUID"})

    user = Users.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200


@app.route("/users", methods=['POST'])
def store_user():
    data = request.get_json()

    if not data or 'name' not in data or 'email' not in data or 'genre' not in data:
        return jsonify({"message": "Missing some attribute"}), 400

    new_user = Users(
        id=str(uuid.uuid4()),
        name=data['name'],
        email=data['email'],
        genre=data['genre']
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201


@app.route('/users/<user_id>', methods=['PATCH'])
def change_user(user_id):
    user = Users.query.get(user_id)

    if user is None:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()

    # only update what finds
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'genre' in data:
        user.genre = data['genre']

    db.session.commit()

    return jsonify(user.to_dict()), 200


@app.route("/users/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    user = Users.query.get(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
