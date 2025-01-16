from src.generic.loader import get_access_id
from src.generic.loader import get_env_variable
from src.generic.private_handler import update_applications
from src.generic.user import remove_credit_from_user
from src.generic.sheets import update_sheet_with_data as __update_sheet_with_data

from src.handler.requester import askGPT35
from src.handler.requester import askGPT4
from src.handler.requester import ask_GPT

from src.handler.sessions import endpoint_add_service_worker
from src.handler.sessions import endpoint_remove_service_worker
from src.handler.sessions import endpoint_authorize_user_for_service_worker
from src.handler.sessions import endpoint_create_session
from src.handler.sessions import endpoint_delete_session
from src.handler.sessions import endpoint_add_operation
from src.handler.sessions import get_available_service_workers


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

from src.operator.proxy import get as __get

from src.generic.api_filing import retrieve, add, update, append

from src.generic.trading import get_btc_price
from src.generic.trading import get_btc_usd_price


DEVELOPMENT = get_env_variable('DEVELOPMENT')
TEXT_STORE_ACCESS_ID = get_access_id()
TEXTS_STORED = {'1': 'The default text stored on initialization'}

if DEVELOPMENT == 'TRUE':
    DB_NAME = 'development.db'
else:
    DB_NAME = 'production.db'


def test(id: str, data: str) -> list[str]:
    if DEVELOPMENT == 'TRUE':
        if DEVELOPMENT == 'TRUE': print(data)
    return True

def google_search(id: str, data: dict) -> list[str]:
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
        prompt = data.get("prompt")
    if not prompt:
        return "request_data is missing 'prompt' parameter."
    return askGPT35(prompt)

def ask_GPT4(id, data):
    prompt = data.get("query", "")
    if not prompt:
        prompt = data.get("prompt")
    if not prompt:
        return "request_data is missing 'prompt' parameter."
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

def get_stored_text(text_id):
    global TEXTS_STORED
    if text_id not in TEXTS_STORED:
        return "text_id route not created yet"
    if DEVELOPMENT == 'TRUE': print("Getting stored text", text_id, TEXTS_STORED[text_id])
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

def add_service_worker(id, data):
    if 'name' not in data:
        return 'Please specify name in request data'
    name = data['name']
    return endpoint_add_service_worker(name)

def remove_service_worker(id, data):
    if 'name' not in data:
        return 'Please specify name in request data'
    name = data['name']
    return endpoint_remove_service_worker(name)

def create_session(id, data):
    if 'username' not in data:
        return 'Please specify username for request data'
    username = data['username']
    return endpoint_create_session(username)

def delete_session(id, data):
    if 'username' not in data:
        return 'Please specify username for request data'
    username = data['username']
    return endpoint_delete_session(username)

# different format
def add_operation(id, data):
    worker_id = data.pop('worker_id')
    operation = data.pop('session_operation')
    
    session_operation_data = {
        'id': id,
        'operation': operation,
        'session_data': data
    }
    if DEVELOPMENT == 'TRUE': print("ADD OPERATION OPERATION:", operation)
    return endpoint_add_operation(worker_id, session_operation_data)

def add_application(id, data):
    if DEVELOPMENT == 'TRUE': print("\n++++++++++++++++\nADD APPLICATION:")
    if DEVELOPMENT == 'TRUE': print("id:", id)
    if DEVELOPMENT == 'TRUE': print("user_id:", data["user_id"])
    update_applications(data["session_id"], data["user_id"], data["description"], data["job_id"], data["url"], data["success"], data["date"])
    
    succeeded = data["success"]
    if succeeded == True:
        remove_credit_from_user(data['user_id'])
        
    return "Applications Updated"

def add_row_to_sheet(id: str, data: dict):
    # adds a row to sheet
    if id != "bilan604":
        return "Invalid ID provided"
    if "sheet_name" not in data:
        return "request_data parameter missing 'sheet_name' parameter."
    if "sheet_name" not in data:
        return "request_data missing 'sheet_name' parameter."
    
    sheet_name = data["sheet_name"]
    sheet_data = data["data"]
    __update_sheet_with_data(sheet_name, sheet_data)
    return "Operation execution completed"

def api_file(id: str, data: dict):
    try:
        action = data['action']
        file_name = data['file_name']
        if action == "retrieve":
            return retrieve(id, file_name)
        if action == "add":
            lines = data['lines']
            if lines and lines[-1] and lines[-1][-1] != "\n":
                lines[-1] += "\n"
            add(id, file_name, lines)
        if action == "update":
            lines = data['lines']
            if lines and lines[-1] and lines[-1][-1] != "\n":
                lines[-1] += "\n"
            update(id, file_name, lines)
        if action == "append":
            line = data['line']
            if line and line[-1] != "\n":
                line += "\n"
            append(id, file_name, line)
            
        return "Completed Successfully"
    except Exception as e:
        return f"Error ocurred: {str(e)}"

def btc_price(id: str, data: dict):
    currency = data['currency']
    return get_btc_price(currency)

def btc_usd_price(id: str, data: dict):
    return get_btc_usd_price()








