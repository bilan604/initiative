import json
import openai
import requests

# If you are git cloning this, you need to replace the following imports with placeholders
# Searches for information
from src.operator.search.searching import get_search_result_links
# Answers the questions
from src.operator.answer.answering import answer_input_questions
# Targets the questions
from src.operator.question.targeting import question_answer_fast
# Uses AI to parse questions
from src.operator.question.advancing import question_answer_prompts, question_answer_prompting

#from src.operator.company.insight import Searcher

# Gets question answers
def do_question_answer_fast(id, data):
    html_content = data["html_content"]
    qas = question_answer_fast(id, html_content)
    return json.dumps(qas)

# Gets prompts to get question answers
def get_question_answer_prompts(id, data):
    print(f"UserId {id} request at get_question_answer_prompts()")
    html_content = data["html_content"]
    prompts = question_answer_prompts(id, html_content)
    return json.dumps(prompts)

# Gets question answers from prompts
def get_question_answer_prompt_responses(id, data):
    print(f"UserId {id} request at get_question_answer_prompt_responses()")
    prompts = data["prompts"]
    api_key = data["api_key"]
    responses = question_answer_prompting(api_key, prompts)
    return json.dumps(responses)

# Gets answered question answers
def do_answer_input_questions(id, data):
    qas = data["qas"]
    answers = answer_input_questions(id, qas)
    return json.dumps(answers)

# Combines 
def get_questions_from_url_with_llm(id, data):
    print(f"UserId {id} request at get_questions_from_url_with_llm()")

    openai_api_key = data.get("api_key", "")
    html_content = ""
    if "html_content" in data:
        html_content = data["html_content"]
    elif "url" in data:
        html_content = requests.get(data["url"]).text
    
    # Gets responses
    prompts = question_answer_prompts(id, html_content)
    qas = question_answer_prompting(openai_api_key, prompts)
    # These are handled, parsed responses
    answers = answer_input_questions(id, qas)
    return json.dumps(answers)

def get_search_result_urls(id, data):
    query = data.get("query", "")
    result_urls = get_search_result_links(query)
    return json.dumps(result_urls)

def get_engineering_growth_insights(id, data):
    username = data.get("username", "")
    password = data.get("password", "")
    company_url = data.get("company_url", "")
    
    #searcher = Searcher(username, password)
    #company = searcher.get_company_information(company_url).to_dict()
    
    # A placeholder
    company = {}
    return json.dumps(company)
