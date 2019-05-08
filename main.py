from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('task')

tasks = {}

class Tasks(Resource):
    def get(self, task_id):
        try:
            task_id = int(task_id)
        except ValueError:
            r = jsonify({'Error':'Task ID is not an int'})
            r.status_code = 401
            return r
        if task_id not in tasks.keys():
            r = jsonify({'Error':'Task does not exist'})
            r.status_code = 404
            return r
        return jsonify({task_id:tasks[task_id]})

    def put(self, task_id):
        if task_id in tasks.keys():
            r = jsonify({'Error':'Task id already exists'})
            r.status_code = 401
            return r
        else:
            args = parser.parse_args()
            tasks[task_id] = args['task']
            return jsonify({task_id:args['task']})

class TasksAll(Resource):
    def get(self):
        return jsonify(tasks)

api.add_resource(Tasks, '/tasks/<string:task_id>')
api.add_resource(TasksAll, '/tasks/')

if __name__ == "__main__":
    app.run(debug=True)