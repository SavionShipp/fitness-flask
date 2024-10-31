from flask import Flask, jsonify, request
from flask_cors import CORS
import db

app = Flask(__name__)
CORS(app)

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