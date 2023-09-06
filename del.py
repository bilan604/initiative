import requests
import json


def t1():
    pars = {
        'id': 'testId',
        'operation': 'test',
        'request_data': json.dumps({
            'key': 'value'
        })
    }
    # string
    resp = requests.post('http://127.0.0.1:5000/api/', params=pars).text
    return resp

def t2():
    pars = {
        'id': 'testId',
        'operation': 'prompt_autoauto',
        'request_data': json.dumps({
            "query": "Say the word 'Recieved'"
        })
    }
    # string
    resp = requests.post('http://127.0.0.1:5000/api/', params=pars).text
    return resp


print(t1())
print(t2())

