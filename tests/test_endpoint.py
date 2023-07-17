import json
import requests
from tests.static_info import *

def api_request(userId, operation, request_data):
    # Specify an endpoint in main
    endpoint = "http://10.0.0.179:8000/api/"

    req_params = {
        "id": userId,
        "operation": operation,
        "request_data": json.dumps(request_data)
    }

    response = requests.get(endpoint, params=req_params)
    print("\nresponse:", response)
    
    return json.loads(response.text)

request_data = {
    "tablename": "input",
    "query": "How many years of Python programming experience do you have?"
}

response = api_request("bilan604", "search_datatable", request_data)
easy_apply_src = get_easy_apply_src()

request_data = {
    "src": easy_apply_src,
    "rule": 'lambda x: "class" in x and "jobs-easy-apply-form-section__grouping" in x["class"]'
}

response = api_request("bilan604", "get_extracted_questions", request_data)

for r in response:
    print("Question:", r["question"])