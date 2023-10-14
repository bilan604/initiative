import os
import json
from datetime import datetime
from flask import Flask, request, redirect, render_template, url_for

from src.handler.loader import update_src_env
from src.generic.loader import get_access_id

# hanlding handles more handle needing functions and args kwargs
from src.handling import test
from src.handling import get_search_result_urls
from src.handling import prompt_autoauto
from src.handling import ask_openai
from src.handling import ask_GPT35, ask_GPT4
from src.handling import get_notefinder
from src.handling import add_notefinder
from src.handling import update_notefinder
from src.handling import create_notefinder
from src.handling import load_notefinder
from src.handling import query_notefinder
from src.handling import update_access
from src.handling import update_stored_text
from src.handling import get_stored_text
from src.handling import get_questions


DEVELOPMENT = False


prev_time = datetime.now()
app = Flask(__name__)


operationFunctionsMap = {
    "test": test,

    "prompt_autoauto": prompt_autoauto,
    "get_search_result_urls": get_search_result_urls,
    "ask_GPT35": ask_GPT35,
    "ask_GPT4": ask_GPT4,

    "get_notefinder": get_notefinder,
    "add_notefinder": add_notefinder,
    "update_notefinder": update_notefinder,
    "create_notefinder": create_notefinder,
    "load_notefinder": load_notefinder,
    "query_notefinder": query_notefinder,
    "update_access": update_access,

    "ask_openai": ask_openai,
    "get_questions": get_questions,
    
    'get_stored_text': get_stored_text,
    "update_stored_text": update_stored_text
}

operationKwargsFunctionsMap = {
    
}

PREV = {operation: datetime.now() for operation in operationFunctionsMap.keys()}
# No cooldown, counts uses, remove other ones someday
ELEVATED = {get_access_id(): 0, "bilan604": 0, "notLan32": 0}

LIMITS = {
    'prompt_autoauto': 60,
    'ask_GPT4': 30,
    'get_search_result_urls': 10
}

def handle_request_params(id, operation, request_data):
    
    def get_seconds_between_datetimes(datetime1, datetime2):
        timedelta = datetime2 - datetime1
        seconds = timedelta.total_seconds()
        return abs(int(seconds))

    global PREV
    global ELEVATED
    global operationFunctionsMap

    # Use actual errors someday maybe
    if operation not in PREV:
        return "Invalid operation paramater specified"

    # last time the operation was used
    prev = PREV[operation]
    curr = datetime.now()
    diff = get_seconds_between_datetimes(prev, curr)
    
    LIMIT = 0
    if operation in LIMITS:
        LIMIT = LIMITS[operation]
    
    if diff < LIMIT:
        if id not in ELEVATED:
            return "Cooldown: "+ str(LIMIT-diff) + " seconds remaining"
        else:
            ELEVATED[id] += 1

    resp = operationFunctionsMap[operation](id, request_data)
    
    # update the previous time
    PREV[operation] = datetime.now()
    return resp


def handle(request):
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

    if DEVELOPMENT == True: print("id:", id)
    if DEVELOPMENT == True: print("operation:", operation)
    if DEVELOPMENT == True: print("request_data:", request_data)

    return handle_request_params(id, operation, request_data)

@app.route("/text_storage/1/", methods=("GET", "POST"))
def text_storage():
    if DEVELOPMENT:
        print("/text_storage/ route called:")

    if request.method == "GET":
        text = get_stored_text('1')
        return text

    if request.method == "POST":
        id = request.args.get('id', None)
        # str
        textStr = request.args.get('request_data', None)
        data = '1' + '||||||||' + textStr
        result = update_stored_text(id, data)
        return json.dumps({
            "message": result
        })

    return "None"

@app.route("/api/", methods=("GET", "POST"))
def api():
    if DEVELOPMENT:
        print("/api/ route called:")

    if request.method == "GET":
        return json.dumps({
            "message": "The format for a get response from API"
        })

    if request.method == "POST":
        response = handle(request)
        api_response = {
            "message": response
        }
        return json.dumps(api_response)

    return "None"

@app.route("/", methods=("GET", "POST"))
def hello_world():
    global prev_time, DEVELOPMENT
    response = ""
    if request.method == "POST":
        query = request.form['query']
        if DEVELOPMENT == True: print("Query: ", query)
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



