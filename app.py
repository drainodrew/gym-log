from flask import Flask, request, jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
import datetime

db = PostgresqlDatabase('gymlog', user='andrewmanuel', password='', host='localhost', port=5432)

class BaseModel(Model):
    class Meta:
        database = db

class Workout(BaseModel):
  name = CharField()
  sets = IntegerField()
  reps = IntegerField()
  pace = CharField()
  date = DateField()

db.connect()
db.drop_tables([Workout])
db.create_tables([Workout])

Workout(name='Alternating Single Arm Incline Dumbbell Bench Press', sets=3, reps=8, pace='20X0', date=datetime.date(2022, 4, 26)).save()
Workout(name='Banded Chainsaw Row', sets=3, reps=8, pace='20X0', date=datetime.date(2022, 4, 26)).save()

# Initialize Flask
# We'll use the pre-defined global '__name__' variable to tell Flask where it is.
app = Flask(__name__)

# Define our route
# This syntax is using a Python decorator, which is essentially a succinct way to wrap a function in another function.
@app.route('/')
def index():
   return "Welcome to Draino's Gym Logs"


@app.route('/workout/', methods=['GET', 'POST'])
@app.route('/workout/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
  if request.method == 'GET':
    if id:
        return jsonify(model_to_dict(Workout.get(Workout.id == id)))
    else:
        workoutList = []
        for workout in Workout.select():
            workoutList.append(model_to_dict(workout))
        return jsonify(workoutList)

  if request.method == 'PUT':
    return 'PUT request'

  if request.method == 'POST':
    new_workout = dict_to_model(Workout, request.get_json())
    new_workout.save()
    return jsonify({"success": True})

  if request.method == 'DELETE':
    return jsonify(Workout.get(Workout.id == id).delete_instance())


app.run(port=9000, debug=True) 
