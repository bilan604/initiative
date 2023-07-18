import re
import json
from src.operator.search.searching import get_search_result_links
from src.operator.search.searching import get_datatable, query_datatable
from src.operator.question.extract import get_questions

"""
This file exists as a wrapper for the functionalities that are accessed,
because inputs have to be verified and stuff, etc

Perhaps it could serve as proxy for a the information in a system design interview?
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
    print("load_datatable()")

    global DATATABLES
    # add validations, etc
    tablename = data
    datatable = get_datatable(id, tablename)
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
    return search_result


def get_extracted_questions(id, data):
    print("get_extracted_questions()")
    # Add validations!

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
        rule_str = re.sub("\\", "", rule_str)
        rule_str = re.sub("\n", "", rule_str)
        rule_str = re.sub("#", "", rule_str)
        rule_str = re.sub("global", "", rule_str)
        if original_str != rule_str:
            return "Bad!"

        script = "global RULE\n"
        script += "RULE = " + rule_str + "\n"
        try:
            exec(script)
        except:
            return "Error on exec(script)"

    questions = get_questions(src, RULE)
    print("\nquestions:", questions)

    return questions
            
    