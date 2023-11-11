from src.generic.loader import get_access_id

from src.handler.loader import get_handler_env

from src.handler.requester import askGPT35
from src.handler.requester import askGPT4

from src.operator.autoauto.AutoAuto import AutoAuto

from src.operator.searching import google_search as __google_search
from src.operator.searching import get_search_result_links
from src.operator.searching import google_search_pages as __google_search_pages

from src.operator.forms import get_questions as __get_questions

from src.operator.nf_operator import __get_notefinder
from src.operator.nf_operator import __add_notefinder
from src.operator.nf_operator import __load_notefinder
from src.operator.nf_operator import __query_notefinder
from src.operator.nf_operator import __update_access

from src.operator.products import get_product_url as __get_product_url
from src.operator.products import get_product_urls as __get_product_urls

from src.handler.requester import ask_GPT

from src.operator.proxy import get as __get


DEVELOPMENT = False
TEXT_STORE_ACCESS_ID = get_access_id()
TEXTS_STORED = {'1': 'The default text stored on initialization'}


if get_handler_env() == 'True':
    DEVELOPMENT = True

def test(id, data):
    if DEVELOPMENT == True:
        print(data)
    return True

def google_search(id, data):
    if "query" not in data:
        return ["No query provided"]
    query = data.get("query", "")
    result_urls = __google_search(query)
    return result_urls

def get_search_result_urls(id, data):
    return google_search(id, data)

def google_search_pages(id, data):
    if "query" not in data:
        return ["No query provided"]
    query = data.get("query", "")
    n = data.get("n", "") # num results
    if not n or type(n) == int:
        n = str(n)
    result_urls = __google_search_pages(query, n)
    return result_urls

def prompt_autoauto(id, data):
    prompt = data.get("query", "")
    objective = prompt
    AGI = AutoAuto(objective)
    AGI.complete_objective()
    return AGI.result

def ask_openai(id, data):
    if 'model' in data:
        return ask_GPT(data['api_key'], data['query'], data['model'])
    return ask_GPT(data['api_key'], data['query'])

def ask_GPT35(id, data):
    prompt = data.get("query", "")
    if not prompt:
        return "[NO_PROMPT_PROVIDED]"
    return askGPT35(prompt)

def ask_GPT4(id, data):
    prompt = data.get("query", "")
    if not prompt:
        return "[NO_PROMPT_PROVIDED]"
    return askGPT4(prompt)

def get_notefinder(id: str, data: dict):
    if "table_name" not in data:
        return "Table name not specified"
    table_name = data["table_name"]
    return __get_notefinder(id, table_name)

def add_notefinder(id: str, data: dict):
    if "table_name" not in data:
        return "Table name not specified"
    if "questions" not in data:
        return "Questions not specified"
    if "answers" not in data:
        return "Answers not specified"
    table_name = data["table_name"]
    questions = data["questions"]
    answers = data["answers"]
    return __add_notefinder(id, table_name, questions, answers)

def update_notefinder(id: str, data: dict):
    return add_notefinder(id, data)

def create_notefinder(id: str, data: dict):
    return add_notefinder(id, data)

def load_notefinder(id: str, data: dict):
    if "table_name" not in data:
        return "Table name not specified"
    table_name = data["table_name"]
    return __load_notefinder(id, table_name)

def query_notefinder(id: str, data: dict):
    if "table_name" not in data:
        return "Table name not specified"
    if "query" not in data:
        return "Query not specified"
    table_name = data["table_name"]
    query = data["query"]
    return __query_notefinder(id, table_name, query)

def update_access(id: str, data: dict):
    if "password" not in data:
        return "password"
    if "access" not in data:
        return "access note specified"
    password = data["password"]
    access = data["access"]
    return __update_access(id, password, access)

def ask_GPT(id: str, data: dict):
    if "api_key" not in data:
        return "API key not specified"
    if "query" not in data:
        return "Query not specified"
    if "model" not in data:
        return "Model not specified"
    return ask_GPT(id, data["api_key"], data["query"], data["model"])

def prompt_stable_diffusion(id: str, data: dict) -> list[str]:
    if "prompt" not in data:
        return "prompt not specified"
    prompt = data["prompt"]
    try:
        resp = __prompt_stable_diffusion(prompt)
        return resp
    except Exception as e:
        return [str(e)]

def get_stored_text(text_id):
    global TEXTS_STORED
    if text_id not in TEXTS_STORED:
        return "text_id route not created yet"
    print("Getting stored text", text_id, TEXTS_STORED[text_id])
    return TEXTS_STORED[text_id]

def update_stored_text(id, data: str):
    global TEXTS_STORED
    if id != TEXT_STORE_ACCESS_ID:
        return "Invalid id"
    if data == None:
        return "request_data not provided"
    # data is the string text
    text_id, text = data.split('||||||||')
    TEXTS_STORED[text_id] = text
    return "Success"

def get_questions(id, data):
    url = ''
    if 'url' in data:
        url = data['url']
    if 'link' in data:
        url = data['link']
    if not url:
        return "No url provided in request data"
    try:
        questions = __get_questions(url)
        return questions
    except Exception as e:
        return f"Error occured: {str(e)}"

def get_product_url(id, data) ->list[str]:
    if "product_description" not in data:
        return "No product_description provided"

    desc = data["product_description"]
    url = __get_product_url(desc)
    return url

def get_product_urls(id, data) ->list[str]:
    if "product_description" not in data:
        return "No product_description provided"

    desc = data["product_description"]
    urls = __get_product_urls(desc)
    return urls

def get(id, data) -> str:
    url = data["url"]
    src = __get(url)
    return src