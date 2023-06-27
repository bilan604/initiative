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
# 
from src.operator.company.insight import load_company_insights

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

def get_company_insights(id, data):
    print("get_company_insights", data, type(data))
    company_profile_url = data.get("profile_url", "")
    insights = load_company_insights(id, company_profile_url)
    return json.dumps(insights)