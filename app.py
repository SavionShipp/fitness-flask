from flask import Flask, request
import db
app = Flask(__name__)


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