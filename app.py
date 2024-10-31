from flask import Flask, jsonify, request
from flask_cors import CORS
import db
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
CORS(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    password = data.get('password')
    
    # Hash the password before storing it
    hashed_password = generate_password_hash(password)
    
    conn = db.connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (name, password) VALUES (?, ?)",
            (name, hashed_password)
        )
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    name = data.get('name')
    password = data.get('password')
    
    conn = db.connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user[2], password):  # `user[2]` corresponds to the password field
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"error": "Invalid name or password"}), 401


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/workouts')
def index():
    return db.workouts_all()

@app.route("/workouts/<id>.json")
def show(id):
    return db.workouts_find_by_id(id)

@app.route("/workouts.json", methods=["POST"])
def create():
    name = request.form.get("name")
    muscle_group = request.form.get("muscle group")
    duration = request.form.get("duration")
    return db.workouts_create(name, muscle_group, duration)

@app.route("/workouts/<id>.json", methods=["PATCH"])
def update(id):
    name = request.form.get("name")
    muscle_group = request.form.get("muscle group")
    duration = request.form.get("duration")
    return db.workouts_update_by_id(id, name, muscle_group, duration)

@app.route("/workouts/<id>.json", methods=["DELETE"])
def destroy(id):
    return db.workouts_destroy_by_id(id)

if __name__ == '__main__':
    app.run(port=5000)