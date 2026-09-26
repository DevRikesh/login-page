from flask import Flask, request, jsonify, render_template
from database import get_connection
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("test_1.html")


@app.route("/login")
def login_page():
    return render_template("test_1.html")


@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Check whether all fields are provided
    if not username or not email or not password:
        return jsonify({
            "success": False,
            "message": "All fields are required"
        }), 400

    # Hash password
    hashed_password = generate_password_hash(password)

    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO users (username, email, password)
            VALUES (%s, %s, %s)
        """

        values = (username, email, hashed_password)

        cursor.execute(query, values)
        connection.commit()

        return jsonify({
            "success": True,
            "message": "Registration successful now signin"
        }), 201

    except Exception as e:

        connection.rollback()

        return jsonify({
            "success": False,
            "message": "Username or email already exists"
        }), 400

    finally:
        cursor.close()
        connection.close()


@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        query = "SELECT * FROM users WHERE email = %s"

        cursor.execute(query, (email,))

        user = cursor.fetchone()

        if user is None:

            return jsonify({
                "success": False,
                "message": "Invalid email or password"
            }), 401

        # Compare entered password with hashed password
        if check_password_hash(user["password"], password):

            return jsonify({
                "success": True,
                "message": "Login successful",
                "username": user["username"]
            }), 200

        else:

            return jsonify({
                "success": False,
                "message": "Invalid email or password"
            }), 401

    finally:

        cursor.close()
        connection.close()


if __name__ == "__main__":
    app.run(debug=True)