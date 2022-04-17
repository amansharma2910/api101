from flask import Flask
from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)
api = Api(app)


TODOS = {
    1: {'task': "Give a presentation"},
    2: {'task': "Hands-on workshop"},
    3: {'task': "Conclude the event"},
}


parser = reqparse.RequestParser()
parser.add_argument('task')


def abort_if_todo_doesnt_exist(todo_id):
    if int(todo_id) not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


class TodoList(Resource):
    def get(self):
        return TODOS, 200

    def post(self):
        args = parser.parse_args()
        todo_id = max(TODOS.keys()) + 1
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201


class Todo(Resource):
    def get(self, todo_id):
        todo_id = int(todo_id)
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id], 200

    def delete(self, todo_id):
        todo_id = int(todo_id)
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        todo_id = int(todo_id)
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201

api.add_resource(TodoList, '/todos/')
api.add_resource(Todo, '/todos/<todo_id>/')


if __name__ == '__main__':
    app.run(debug=True)