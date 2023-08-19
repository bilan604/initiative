import os
import json
from flask import Flask, request, redirect, render_template, url_for
from src.handling import get_search_result_links
from src.handling import search_datatable
from src.handling import get_extracted_questions
from dotenv import load_dotenv
load_dotenv()

# count is unused
count = 0

app = Flask(__name__)

operationFunctionsMap = {
    # Utility function
    "get_search_result_links": get_search_result_links,
    "search_datatable": search_datatable,
    "get_extracted_questions": get_extracted_questions
}


def operationFunctionHandler(requestorId, operation, requestData):
    print("requestorId:", requestorId)
    print("operation:", operation)
    return operationFunctionsMap[operation](requestorId, requestData)


@app.route("/api/", methods=("GET", "POST"))
def api():
    print("==> api() function called")
    userId = request.args.get("id")
    operation = request.args.get("operation")
    request_data = json.loads(request.args.get("request_data"))

    if request.method == "GET":
        print("GET", userId, operation)
        api_response = operationFunctionHandler(userId, operation, request_data)
        return json.dumps(api_response)
    
    elif request.method == "POST":
        print("POST", userId, operation)
        api_response = operationFunctionHandler(userId, operation, request_data)
        return json.dumps(api_response)
    
    return "None"


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        return "TBH"
    return render_template("index.html")


def run_app():
    path = "/".join(os.getcwd().split("\\"))
    os.chdir(path)
    try:
       app.run(host="10.0.0.179", port=8000)
    except:
        app.run()

