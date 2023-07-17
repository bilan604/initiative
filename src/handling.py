import json
import requests
from src.operator.search.searching import get_search_result_links
from src.operator.search.searching import get_datatable, query_datatable
from src.operator.question.extract import get_questions

"""
This file exists as a wrapper for the functionalities that are accessed,
because inputs have to be verified and stuff, etc
"""


RULE = ""
DATATABLES = {}


def get_search_result_links(id, data):
    query = data.get("query", "")
    result_urls = get_search_result_links(query)
    return json.dumps(result_urls)


def load_datatable(id, data):
    """
    Loads to RAM, is placeholder, replaceable component
    """
    print("load_data()")
    print("data:", data)
    print("\ntype(data):", type(data))

    global DATATABLES
    # add validations, etc
    tablename = data
    datatable = get_datatable(id, tablename)
    DATATABLES[tablename] = datatable


def search_datatable(id, data):
    print("load_data()")
    print("data:", data)
    print("\ntype(data):", type(data))

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
    return search_result


def get_extracted_questions(id, data):
    print("load_data()")
    print("data:", data)
    print("\ntype(data):", type(data))

    # validations, etc
    # validations, etc
    # validations, etc!

    src = data["src"]
    if not src:
        return "not src"
    
    rule_str = data["rule"]
    
    global RULE
    RULE = None
    if not rule_str:
        return "not rule_str"
    else:
        script = "global RULE\n"
        script += "RULE = " + rule_str + "\n"
        print("\nscript:", script)        
        try:
            exec(script)
        except:
            return "Error on exec(script)"
    
    print("\nrule:", RULE)

    questions = get_questions(src, RULE)
    
    print("\nquestions:", questions)

    return questions
            
    