import os
import json
from flask import request, Flask
from flask import render_template
from flask import redirect
from flask import url_for
from src.generic.turtle import Turtle

# The environment variable setter for console logs (placeholder)
from src.handler.loader import update_src_env

# import functionalities for all the operations for from src/handling.py
from src.handling import test
from src.handling import hello_world
from src.handling import your_api_functionality


DEVELOPMENT = False


app = Flask(__name__)

# I created a turtle to help limit how frequently processes can be called
# to prevent bugs, spam, DOS/DDOSes from maxing out the server's CPU utilization
turtle = Turtle()

# specify all the functions imported from handling in this map
# in order to use them
operationFunctionsMap = {
    "test": test,
    "hello_world": hello_world,
    "your_api_functionality": your_api_functionality
}

turtle.limits = {
    # sets a 5 second limit on requests to the test operation
    'test': 5  
    # operations not specified default to 1 second
}


def handle_request_params(id, operation, request_data):
    global turtle
    global operationFunctionsMap

    if not turtle.canOperate(operation):
        rem = turtle.getRemaining(operation)
        return "Cooldown: " + str(rem) + " seconds remaining"
    
    resp = operationFunctionsMap[operation](id, request_data)

    # update the turtle!
    turtle.updateOperation(operation)
    
    return resp


def handle(request):
    global turtle
    if not turtle.can():
        return "Cooldown: 1 second remaining"
    
    id = request.args.get("id", None)
    if id == None:
        return "Parameter: 'id' not specified"
    operation = request.args.get("operation", None)
    if operation == None:
        return "Parameter: 'operation' not specified"
    request_data = request.args.get("request_data", None)
    if request_data == None:
        return "Parameter: 'request_data' not specified"
    request_data = json.loads(request_data)

    resp = handle_request_params(id, operation, request_data)

    # update the turtle!
    turtle.update()
    
    return resp


@app.route("/api/", methods=("GET", "POST"))
def api():
    global DEVELOPMENT
    if DEVELOPMENT:
        print("/api/ route called:")
    
    if request.method == "GET":
        return json.dumps({
            "message": "You have reached the API route!"
        })

    if request.method == "POST":
        response = handle(request)
        api_response = {
            "message": response
        }
        return json.dumps(api_response)

    return json.dumps({
            "message": "This condition will only trigger when more methods are added!"
        })


@app.route("/", methods=("GET", "POST"))
def hello_world():
    global DEVELOPMENT
    # handle rerenders of the same route by submitting a post request to
    # the route's function and handling the post request functionality
    # with the universal handle_request_params function
    response = ""
    if request.method == "POST":
        query = request.form['query']
        if query and len(query) > 0:
            response = handle_request_params('', 'prompt_autoauto', {
                "query": query
            })
        return render_template('index.html', prompt_response=response)
    
    return render_template('index.html')


# When working locally, this application should be run by running main.py
# so that the environment is set to 'development'

# This application is not run from main.py in production.
def run_app(environment):
    global DEVELOPMENT
    
    if environment == 'development':
        DEVELOPMENT = True
    
    update_src_env(DEVELOPMENT)

    # set the path to absolute in all repositories
    # by changing the path to the current path at flask app
    path = "/".join(os.getcwd().split("\\"))
    os.chdir(path)
    
    app.run()
