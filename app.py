from flask import Flask, request, jsonify

app = Flask(__name__)

users = {
    1: {"id": 1, "name": "John Doe", "email": "john@example.com"},
    2: {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
}

def get_next_id():
    return max(users.keys()) + 1 if users else 1

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values()))

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    if not request.json or 'name' not in request.json or 'email' not in request.json:
        return jsonify({"error": "Bad request"}), 400
    
    new_id = get_next_id()
    user = {
        "id": new_id,
        "name": request.json['name'],
        "email": request.json['email']
    }
    users[new_id] = user
    return jsonify(user), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    if not request.json:
        return jsonify({"error": "Bad request"}), 400
    
    user['name'] = request.json.get('name', user['name'])
    user['email'] = request.json.get('email', user['email'])
    return jsonify(user)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
