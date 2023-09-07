from src.operator.searching import get_search_result_links
from src.operator.autoauto.AutoAuto import AutoAuto


def test(id, data):
    print(data)
from src.handler.loader import get_handler_env


DEVELOPMENT = False
if get_handler_env() == 'True':
    DEVELOPMENT = True


def test(id, data):
    # Handle the http request as if it were a normal http request here.
    if DEVELOPMENT == True:
        print(data)
    # return the response to the request, which will be handled in the request handler in flask_app.py
    return True


def prompt_autoauto(id, data):
    prompt = data.get("query", "")
    objective = prompt
    AGI = AutoAuto(objective)
    AGI.complete_objective()
    return AGI.result
if DEVELOPMENT == True:
    from src.operator.searching import get_search_result_links
    from src.operator.autoauto.AutoAuto import AutoAuto


    def get_search_result_links(id, data):
        query = data.get("query", "")
        result_urls = get_search_result_links(query)
        return result_urls

    def prompt_autoauto(id, data):
        prompt = data.get("query", "")
        objective = prompt
        AA = AutoAuto(objective)
        AA.complete_objective()
        return AA.result




