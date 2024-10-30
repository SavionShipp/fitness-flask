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