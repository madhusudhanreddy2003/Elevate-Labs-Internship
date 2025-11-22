from flask import Flask, request, jsonify

app = Flask(__name__)

users = {}
next_id = 1


def get_next_id():
    global next_id
    _id = next_id
    next_id += 1
    return _id


@app.route("/")
def home():
    return jsonify({"message": "User API is running"})


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(list(users.values())), 200


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    name = data.get("name")
    email = data.get("email")
    age = data.get("age")

    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400

    user_id = get_next_id()
    user = {
        "id": user_id,
        "name": name,
        "email": email,
        "age": age
    }
    users[user_id] = user
    return jsonify(user), 201


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    if "name" in data:
        user["name"] = data["name"]
    if "email" in data:
        user["email"] = data["email"]
    if "age" in data:
        user["age"] = data["age"]

    return jsonify(user), 200


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    del users[user_id]
    return jsonify({"message": f"User {user_id} deleted"}), 200


if __name__ == "__main__":
    print("Running Task 4 Flask App")
    print(app.url_map)
    app.run(debug=True)


