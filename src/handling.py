import json
import openai
import requests
# Searches for information
from src.operator.search.searching import get_search_result_links
# Answers the questions
from src.operator.answer.answering import answer_input_questions
# Targets the questions
from src.operator.question.targeting import question_answer_fast
# Get it? Advances the question to a third party.
from src.operator.question.advancing import question_answer_prompts, question_answer_prompting


def get_question_answer_prompts(id, data):
    html_content = data["html_content"]
    prompts = question_answer_prompts(id, html_content)
    return json.dumps(prompts)

def get_question_answer_prompt_responses(id, data):
    prompts = data["prompts"]
    responses = question_answer_prompting(id, prompts)
    return json.dumps(responses)

def get_questions_from_url_with_llm(id, data):
    # a combination 
    if type(data) == str:
        data = json.loads(data)
    if "api_key" not in data:
        return "No api key provided"
    openai_api_key = data["api_key"]
    
    if "url" in data:
        html_content = requests.get(data["url"]).text
    elif "html_content" in data:
        html_content = data["html_content"]
    else:
        return "No webpage specified"

    prompts = question_answer_prompts(id, html_content)
    # These are handled, parsed responses
    responses = get_question_answer_prompt_responses(openai_api_key, prompts)
    return json.dumps(responses)


def do_question_answer_fast(id, data):
    html_content = data["html_content"]
    qas = question_answer_fast(id, html_content)
    return json.dumps(qas)


def do_answer_input_questions(id, data):
    qas = data["qas"]
    answers = answer_input_questions(id, qas)
    return json.dumps(answers)


def get_search_result_urls(id, data):
    if type(data) == str:
        data = json.loads(data)
    query = data["query"]
    result_urls = get_search_result_links(query)
    return result_urls