import os
import json
from datetime import datetime
from flask import Flask, request, redirect, render_template, url_for

from src.handler.loader import update_src_env

from src.handling import test
from src.handling import get_search_result_links
from src.handling import prompt_autoauto

DEVELOPMENT = False
prev_time = datetime.now()
app = Flask(__name__)

def get_seconds_between_datetimes(datetime1, datetime2):
    timedelta = datetime2 - datetime1
    seconds = timedelta.total_seconds()
    return abs(int(seconds))

operationFunctionsMap = {
    "test": test,
    "prompt_autoauto": prompt_autoauto,
    "get_search_result_links": get_search_result_links
}

def handle_request_params(id, operation, request_data):
    curr = datetime.now()
    global prev_time
    diff = get_seconds_between_datetimes(prev_time, curr)

    if diff < 15:
        return "Cooldown: "+ str(15-diff) + " seconds remaining"

    resp = operationFunctionsMap[operation](id, request_data)
    prev_time = datetime.now()
    return resp

def handle(request):
    id = request.args.get("id", None)
    operation = request.args.get("operation", None)
    request_data = request.args.get("request_data", None)
    request_data = json.loads(request_data)

    if DEVELOPMENT == True:  print("id:", id)
    if DEVELOPMENT == True: print("operation:", operation)
    if DEVELOPMENT == True: print("request_data:", request_data)

    return handle_request_params(id, operation, request_data)

@app.route("/api/", methods=("GET", "POST"))
def api():
    if DEVELOPMENT:
        print("/api/ route called:")

    if request.method == "GET":
        return json.dumps({
            "message": "The format for a get response from API"
        })

    elif request.method == "POST":
        response = handle(request)
        api_response = {
            "message": response
        }
        return json.dumps(api_response)

    return "None"

@app.route("/", methods=("GET", "POST"))
def hello_world():
    global prev_time
    response = ""
    if request.method == "POST":
        query = request.form['query']
        print("Query", query)
        if query and len(query) > 0:
            response = handle_request_params('', 'prompt_autoauto', {
                "query": query
            })
        return render_template('index.html', prompt_response=response)
    
    return render_template('index.html', prompt_response=response)

# a function to run this app from main.py
def run_app(environment):
    global DEVELOPMENT
    path = "/".join(os.getcwd().split("\\"))
    if environment == 'development':
        
        DEVELOPMENT = True
    update_src_env(DEVELOPMENT)            
    os.chdir(path)
    app.run()



