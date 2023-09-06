from src.operator.searching import get_search_result_links
from src.operator.autoauto.AutoAuto import AutoAuto


def test(id, data):
    print(data)
    return True

def get_search_result_links(id, data):
    query = data.get("query", "")
    result_urls = get_search_result_links(query)
    return result_urls

def prompt_autoauto(id, data):
    prompt = data.get("query", "")
    objective = prompt
    AGI = AutoAuto(objective)
    AGI.complete_objective()
    return AGI.result




