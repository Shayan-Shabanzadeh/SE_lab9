from flask import Flask, request, jsonify

app = Flask(__name__)

users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Doe", "email": "jane@example.com"}
]


@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.get_json()
    users.append(new_user)
    return jsonify({"message": "User created successfully"}), 201


# Read all users
@app.route('/users', methods=['GET'])
def get_all_users():
    return jsonify(users)


# Read a specific user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"message": "User not found"}), 404


# Update a user by ID
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        updated_user = request.get_json()
        user.update(updated_user)
        return jsonify({"message": "User updated successfully"})
    return jsonify({"message": "User not found"}), 404


# Delete a user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [u for u in users if u['id'] != user_id]
    return jsonify({"message": "User deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)
