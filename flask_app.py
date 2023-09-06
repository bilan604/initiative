import os
import json
from datetime import datetime
from flask import Flask, request, redirect, render_template, url_for

from src.handling import get_search_result_links
from src.handling import search_datatable
from src.handling import get_extracted_questions
from src.handling import prompt_autoauto


prev_time = datetime.now()
app = Flask(__name__)


def get_seconds_between_datetimes(datetime1, datetime2):
    timedelta = datetime2 - datetime1
    seconds = timedelta.total_seconds()
    return int(seconds)

operationFunctionsMap = {
    # Utility function
    "get_search_result_links": get_search_result_links,
    "search_datatable": search_datatable,
    "get_extracted_questions": get_extracted_questions,
    "prompt_autoauto": prompt_autoauto
}

def handle(requestorId, operation, requestData):
    print("requestorId:", requestorId)
    print("operation:", operation)
    return operationFunctionsMap[operation](requestorId, requestData)


@app.route("/api/", methods=("GET", "POST"))
def api():
    print("==> api() function called")
    userId = request.args.get("id")
    print("userId:", userId)
    operation = request.args.get("operation")
    print("operation:", operation)
    request_data = json.loads(request.args.get("request_data"))
    print("request_data:", request_data)
    if request.method == "GET":
        print("GET", userId, operation)
        api_response = handle(userId, operation, request_data)
        return json.dumps(api_response)
    
    elif request.method == "POST":
        print("POST", userId, operation)
        api_response = handle(userId, operation, request_data)
        return json.dumps(api_response)
    
    return "None"


@app.route("/", methods=("GET", "POST"))
def hello_world():
    if request.method == "POST":
        global prev_time
        curr = datetime.now()
        diff = get_seconds_between_datetimes(prev_time, curr)
        if diff < 15:
            return render_template('index.html', prompt_response="")
        data = {
            "query": request.form["query"]
        }
        response = handle("", "prompt_autoauto", data)
        prev_time = curr
        return render_template("index.html", prompt_response=response)
    
    return render_template('index.html', prompt_response="")
    


# a function to run this app from main.py
def run_app():
    path = "/".join(os.getcwd().split("\\"))
    os.chdir(path)
    app.run()

