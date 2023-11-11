import os
import json
from flask import Flask, request, redirect, render_template, url_for

from src.generic.loader import get_access_id
from src.generic.turtle import Turtle

from src.handler.loader import update_src_env

# hanlding handles more handle-needing functions along with their args kwargs
from src.handling import test
from src.handling import get
from src.handling import google_search
from src.handling import google_search_pages
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
from src.handling import get_product_url
from src.handling import get_product_urls


DEVELOPMENT = False


app = Flask(__name__)
operationFunctionsMap = {
    "test": test,

    "get": get,

    "ask_GPT35": ask_GPT35,
    "ask_GPT4": ask_GPT4,
    "prompt_autoauto": prompt_autoauto,
    "ask_openai": ask_openai,

    "google_search": google_search,
    "get_search_result_urls": get_search_result_urls,
    "google_search_pages": google_search_pages,
    "get_n_search_results": google_search_pages,

    "get_questions": get_questions,

    "get_notefinder": get_notefinder,
    "add_notefinder": add_notefinder,
    "update_notefinder": update_notefinder,
    "create_notefinder": create_notefinder,
    "load_notefinder": load_notefinder,
    "query_notefinder": query_notefinder,
    "update_access": update_access,

    'get_stored_text': get_stored_text,
    "update_stored_text": update_stored_text,

    "get_product_url": get_product_url,
    "get_product_urls": get_product_urls
}

turtle = Turtle()
turtle.limits = {
    'get': 5,
    'ask_GPT35': 30,
    'ask_GPT4': 30,
    'ask_openai': 30,
    'prompt_autoauto': 60,
    'google_search': 5,
    'get_search_result_urls': 5,
    'google_search_pages': 10,
    'get_n_search_results': 10
}


def handle_request_params(id, operation, request_data):
    global turtle
    global operationFunctionsMap

    if not turtle.canOperate(operation):
        rem = turtle.getRemaining(operation)
        return "Cooldown: "+ str(rem) + " seconds remaining"
    
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

    if DEVELOPMENT == True: print("id:", id)
    if DEVELOPMENT == True: print("operation:", operation)
    if DEVELOPMENT == True: print("request_data:", request_data)

    resp = handle_request_params(id, operation, request_data)

    # update the turtle!
    turtle.update()
    
    return resp

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
