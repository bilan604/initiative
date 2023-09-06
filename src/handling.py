from src.handler.loader import get_handler_env
from src.operator.searching import get_search_result_links
from src.operator.autoauto.AutoAuto import AutoAuto


DEVELOPMENT = False
if get_handler_env() == 'True':
    DEVELOPMENT = True

def test(id, data):
    if DEVELOPMENT == True:
        print(data)
    return True

def get_search_result_links(id, data):
    query = data.get("query", "")
    result_urls = get_search_result_links(query)
    return result_urls

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




