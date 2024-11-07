# ProjectsAPI! (API Documentation, Tutorial, and Template)
@Author: Xing Yang Lan

## Intro:

[The Website](http://bilan604.pythonanywhere.com)  

The purpose of this project is to so that I can bundle code I've written across different sub-projects into one place, and then make post requests to the functionality by specifying both the functionality and the inputs required for that functionality. Hosting it online allows me to access code from different machines and by logging in to use the operator interface I can control programs in real time from my phone.

## Cloning
```
git clone https://github.com/bilan604/initiative.git
cd ./initiative
```
```
python -m pip install -r requirements.txt
```
```
python main.py
```

## Post Request Format  

The /api/ endpoint handles POST request that must contain the three parameters "id", "operation", and "request_data". The ID specifies the user, Operation specifies what functionality should be done, and request_data specifies the inputs for the functionality.

#### CURL:
```
curl -X POST "https://bilan604.pythonanywhere.com/api/" \
     -H "Content-Type: application/json" \
     -d '{ "id": "bilan604", "operation": "get_search_result_urls", "request_data": {"query": "Fun things to do in Argentina"}}'
```

#### Python:
```
import json
import requests

def use_api_dev(pars):
    resp = requests.post(f'https://bilan604.pythonanywhere.com/api/', params=pars).text
    return json.loads(resp)["message"]

pars = {
    "id": "bilan604",
    "operation": "get_search_result_urls",
    "request_data": json.dumps({
        'query': 'Fun things to do in Argentina'
    })
}

print(use_api_dev(pars))
```

## Some Functionalities

#### Search Results:

Returns the first page of urls for a given search query.

```
    pars = {
        'id': '',
        'operation': 'get_search_result_urls',
        'request_data': json.dumps({
            'query': '[string: the search query]',
        })
    }
```
response: A message containing a list of search result urls

Returns the first n urls for a given search query.
```
    pars = {
        'id': '',
        'operation': 'get_n_search_results',
        'request_data': json.dumps({
            'query': '[string: the search query]',
            'n': [integer: desired number of results]
        })
    }
```
response: A message containing a list of n search result urls

#### Automation

I can an endpoint (https://bilan604.pythonanywhere.com/apply/) to control a Selenium program that searches and answers questions online for me using GPT-4.

https://github.com/bilan604/ProjectsAPI/assets/77251582/3a2d10cf-391c-4dd1-b380-9d3b06dd1e5a


