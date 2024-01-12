from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import yaml


app = Flask(__name__)
with open('config.yaml', 'r') as config_file:
    config_data = yaml.safe_load(config_file)

app.config['SQLALCHEMY_DATABASE_URI'] = config_data['database']['uri']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config_data['database']['track_modifications']


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)


@app.route('/users', methods=['POST'])
def create_user():
    new_user_data = request.get_json()
    new_user = User(**new_user_data)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201


# Read all users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users_data = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
    return jsonify(users_data)


# Read a specific user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        user_data = {"id": user.id, "name": user.name, "email": user.email}
        return jsonify(user_data)
    return jsonify({"message": "User not found"}), 404


# Update a user by ID
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        updated_user_data = request.get_json()
        user.name = updated_user_data.get('name', user.name)
        user.email = updated_user_data.get('email', user.email)

        db.session.commit()
        return jsonify({"message": "User updated successfully"})
    return jsonify({"message": "User not found"}), 404


# Delete a user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
    return jsonify({"message": "User not found"}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
