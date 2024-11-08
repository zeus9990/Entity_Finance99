from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta
from database import get_user, lb

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "mysecret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)  # Set token expiry to 30 minutes
jwt = JWTManager(app)

# Sample user data
users = {
    "user1": "password1",
}

# Login route
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username not in users or users[username] != password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

# Custom handler for expired tokens
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"msg": "Token has expired"}), 401


# Protected route
@app.route("/leaderboard", methods=["GET"])
@jwt_required()
def leaderboard():
    get_jwt_identity()
    header_value = int(request.headers.get('value'))
    response = lb(header_value)
    return jsonify(response)

@app.route("/userpoints", methods=["GET"])
@jwt_required()
def userdata():
    get_jwt_identity()
    header_value = request.headers.get('user_id')
    response = get_user(int(header_value))
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
