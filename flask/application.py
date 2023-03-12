from flask import Flask
from flask import render_template
from flask_cors import CORS
from flask import request


application = Flask(__name__)
CORS(application)


@application.post('/create-todo')
def create_todo():
    print(request.data)
    return "OK"


@application.get('/get-todos')
def get_todo():
    data = [{
            "id": 0,
            "todo": "mi primer todo",
            "completed": False,
            },
            {
            "id": 1,
            "todo": "mi segundo todo",
            "completed": False,
            },
            {
            "id": 2,
            "todo": "mi tercer todo",
            "completed": False,
            }
            ]
    return data


@application.put('/complete-todo')
def complete_todo():
    pass


# @application.route('/')
# def hello_world():
#     return "<p>Hello world</p>"


# @application.route('/nombre')
# def retornar_nombre():
#     return "<div>Guillermo</div>"


# @application.route('/usuario/<username>')
# def retornar_parametro(username):
#     return render_template("hello.html", username=username)


# @application.post('/')
# def hello_world_post():
#     return "<h1>Hello world</h1>"
