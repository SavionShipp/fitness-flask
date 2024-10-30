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
    type = request.form.get("type")
    duration = request.form.get("duration")
    return db.workouts_create(name, type, duration)

@app.route("/workouts/<id>.json", methods=["PATCH"])
def update(id):
    name = request.form.get("name")
    type = request.form.get("type")
    duration = request.form.get("duration")
    return db.workouts_update_by_id(id, name, type, duration)

@app.route("/workouts/<id>.json", methods=["DELETE"])
def destroy(id):
    return db.workouts_destroy_by_id(id)

if __name__ == '__main__':
    app.run(port=5000)