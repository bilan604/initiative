import json
import requests


def test_src():
    url = "https://docs.google.com/forms/d/e/1FAIpQLScMDHIfobvFjHrOXTwERHskYutiCzgBfA6iAQBkRlijXT92MA/viewform"    
    src = requests.get(url).text
    req_params = {
    "userId": "testId",
    "operation": "get_question_answer_prompts",
    "requestData": json.dumps({
            "html_content": src
            })
    }        
    response = requests.get("http://10.0.0.179:8000/api/", params=req_params)
    print(response.text)
    return response.text


def test_url(api_key):

    url = "https://docs.google.com/forms/d/e/1FAIpQLScMDHIfobvFjHrOXTwERHskYutiCzgBfA6iAQBkRlijXT92MA/viewform"
    
    req_params = {
    "userId": "testId",
    "operation": "get_questions_from_url_with_llm",
    "requestData": json.dumps({
            "api_key": api_key,
            "url": url
            })
    }
    response = requests.get("http://10.0.0.179:8000/api/", params=req_params)
    print(response.text)
    print("test2: len(response.text)", len(response.text))
    
