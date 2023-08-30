import json
import openai

from src.handler.load.loading import check_contains
from src.operator.search.searching import get_search_result_links
from src.operator.search.searching import get_datatable, query_datatable
from src.operator.question.extract import get_questions
from src.operator.autoauto.AutoAuto import AutoAuto


RULE = ""
DATATABLES = {}

def get_env(file_path=".env"):
    env = {}
    with open(file_path, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line:
                lst = line.split("=")
                env[lst[0].strip()] = lst[1].strip()
    return env

openai.api_key = get_env()["OPENAI_API_KEY"].strip()

def get_search_result_links(id, data):
    query = data.get("query", "")
    result_urls = get_search_result_links(query)
    return json.dumps(result_urls)


def load_datatable(id, data):
    global DATATABLES

    # add validations, etc
    id_present = check_contains("src/storage", id)
    if not id_present:
        return f"No datatables for id: {id}"

    tablename = data
    datatable = get_datatable(id, tablename)
    print("\ndatatable:", datatable)
    DATATABLES[tablename] = datatable


def search_datatable(id, data):
    print("search_datatable()")

    # validations, etc
    tablename = data["tablename"]
    if not tablename:
        return "not tablename"
    
    query = data["query"]
    if not query:
        return "not query"
    
    if tablename not in DATATABLES:
        print("tablename not in DATATABLES")
        print("AUTOMATICALLY LOADING DATATABLE")
        load_datatable(id, tablename)
        
    search_result = query_datatable(query, DATATABLES[tablename])
    print("\nsearch_result:", search_result)
    return search_result


def get_extracted_questions(id, data):
    print("get_extracted_questions()")

    src = data["src"]
    if not src:
        return "not src"
    
    rule_str = data["rule"]
    original_str = rule_str

    global RULE
    RULE = None
    if not rule_str:
        return "not rule_str"
    else:
        script = "global RULE\n"
        script += "RULE = " + rule_str + "\n"
        try:
            exec(script)
        except:
            return "Error on exec(script)"
    
    if not RULE:
        return "not RULE"

    questions = get_questions(src, RULE)
    
    return questions


def prompt_autoauto(id, data):
    prompt = data.get("query", "")
    objective = prompt
    print(objective)

    AGI = AutoAuto(objective)
    AGI.complete_objective()

    print("\n===================>:")
    print(AGI.result)
    print("---------fin----------")
    
    return AGI.result




