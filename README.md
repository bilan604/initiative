# python-server

A Python Flask Server and flask server template for aggregating parallel processes. By aggregating various functionalities into a backend which is hosted online, I can access my code accross devices, virtual envs, and repositories.  

View Most recent build running:  
[Website](http://bilan604.pythonanywhere.com)  

## Requirements
1. git bash
2. python version 3.11

## Running the Server:
1. Navigate to where you want the folder to be and clone the repository.
```
git clone https://github.com/bilan604/initiative.git
```

2. Navigate to the folder
```
cd initiative
```

3. Install the requirements
```
pip install -r requirements.txt
```

4. Run main.py from git bash.
```
python main.py
```

Running main.py locally automatically sets the environment variable in handling to True. The app is run from flask_app.py in production.  

## Troubleshooting  
If you encounter any errors, try checking the Python version  
```
python --version
```

or upgrading pip. Older versions of packages can cause code to behave unexpectedly, sometimes without warning.
```
pip install --upgrade pip
```

## Calling the API  

Here is the post request format for calling the API:  
```
import json
import requests

URL = 'http://bilan604.pythonanywhere.com'

def get_questions(url: str) -> list[dict]:
    pars = {
        "id": "bilan604",
        "operation": "get_questions",
        "request_data": json.dumps({
            'url': url
        })
    }
    resp = requests.post(f'{URL}/api/', params=pars)
    if resp.status_code == 200:
        message = json.loads(resp.text)
        questions = message["message"]
        return questions
    print("Error:")
    print(resp.text)
    return []
```

Here is an example of one of the functionalities, get_questions, which loads user input questions given a url in a form agnostic manner.  

![Loading Questions from a webpage](https://github.com/bilan604/initiative/blob/main/static/using_api.png)  


## Operations:  

These endpoints don't require and id and are free to use, but there is a rate limiter for requests. Feel free to try them out or continue using as much as neccessary. :)   

#### SERP API:

Returns the first page of urls for a search result.

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

#### SERP API Again:

Tries to get n urls for search results, for a maximum of n=100 urls.

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

#### HTML User Input Element Scrapper:

Good for selenium based projects.

```
    pars = {
        "id": "",
        "operation": "get_questions",
        "request_data": json.dumps({
            'url': url
        })
    }
```
response: a list of objects containing the question, html type of the question element of the question, and a list of the answer options (a list containing the label for the option and the element of the option) if present
