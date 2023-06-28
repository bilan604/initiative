import os
import json
from src.handling import *
from flask import Flask, request, redirect, render_template, request, url_for
from dotenv import load_dotenv
load_dotenv()


count = 0
app = Flask(__name__)


operationFunctionsMap = {
    # Wrapper function: getUrlQuestionsWithLLM
    "get_question_answer_prompts": get_question_answer_prompts,
    # Wrapper function: getUrlQuestionsWithLLM
    "get_question_answer_prompt_responses": get_question_answer_prompt_responses,
    # Requires API Key
    "get_questions_from_url_with_llm": get_questions_from_url_with_llm,

    "question_answer_fast": do_question_answer_fast, 
    "answer_input_questions": do_answer_input_questions,
    # Utility function
    "get_search_result_links": get_search_result_urls,

    "get_company_insights": get_company_insights
}


def operationFunctionHandler(requestorId, operation, requestData):
    print("requestorId:", requestorId)
    print("operation:", operation)
    return operationFunctionsMap[operation](requestorId, requestData)


@app.route("/api/", methods=("GET", "POST"))
def api():
    print("Function call, api()")
    if request.method == "GET":
        userId = request.args.get("id")
        operation = request.args.get("operation")
        requestData = json.loads(request.args.get("requestData"))
        print("GET", userId, operation)
        appResponse = operationFunctionHandler(userId, operation, requestData)
        return json.dumps(appResponse)
    elif request.method == "POST":
        data = request.json
        userId = data.get("id", "")
        operation = data.get("operation", "")
        requestData = data.get("requestData", "")
        print("POST", userId, operation)
        return operationFunctionHandler(userId, operation, requestData)
    
    return "None"


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        return "TBH"
    return render_template("index.html")

def run_app():
    path = "/".join(os.getcwd().split("\\"))
    os.chdir(path)
    app.run(host="10.0.0.179", port=8000)


    

