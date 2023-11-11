# Take Initiative! (API Documentation, Tutorial, and Template)
@Author: Xing Yang Lan

## Intro:
I started this project because I realized that a lot of the code I was writting for unrelated personal projects, for fun, and for assigned projects were similar in nature, but not concrete enough or important enough to make a Github repository for. 

Realizing that this could be overcome by placing the repetitive functionalities from different repositories together in a single repository, I decided to make an API and aggregate isolated functionalities from old projects into this single project, but instead of making seperate API routes for them, just giving each functionality a name for the operation that it performs.

Now, the flask server url below is backend API endpoint for me and my friends' projects - allowing functionalities to be accessed without git cloning or pip installations in remote environments.

[Landing Page](http://bilan604.pythonanywhere.com)  

NOTE: This repository isn't the actual repository for the url above. Since I added the code for most of the functionalities in the .gitignore, but wanted to make the repository public as well, I have changed this repository so that it is basically a flask tutorial to help people get into Python/Flask. (Its more exciting than learning for loops! :D)

## System Requirements
Python 3.11
Node.js v18.15.0
Git Bash
Internet Connection
5 minutes

## Installation Requirements (Python Modules)

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

4. To install the Python Modules run ```pip install requirements.txt``` in the bash console.  

## Running  
Git Bash
```
python main.py
```

Running main.py locally automatically sets the environment variable in handling to True. The app is run from flask_app.py in production. 

## Troubleshooting  
If you encounter any errors installing requirements from ```requirements.txt``` just use pip to install them mannually like ```pip install beautifulsoup4``.

The above issue may be caused by not having a high enough version of Python. You can check your version using:
```
python --version
```

Try upgrading pip:
```
pip install --upgrade pip
```

If you have multiple versions, make sure that the Python interpreter is using the right version of Python (ctrl+shift+p if you are using vscode).

You can also specify a specific version of Python if you have multiple versions of Python in git bash like ```python3.11 -m pip install beautifulsoup4```. If you do this, please not that each version of Python you have installed has its own version of pip!.
```
python3.11 -m pip install --upgrade pip
```

## Post Request Format  

The /api/ endpoint takes an id, the desired functionality (similar to specifying 'Content-Type' in the headers for a post request, but for the route itself), and the request_data which is a json string containing the parameters for the function.

```
import json
import requests

def use_api(pars: dict) -> list[dict]:
    resp = requests.post(f'http://bilan604.pythonanywhere.com/api/', params=pars).text
    return json.loads(resp)["message"]

pars = {
    "id": "bilan604",
    "operation": "get_search_result_urls",
    "request_data": json.dumps({
        'query': 'What is the capital of Argentina?'
    })
}
print(use_api(pars))
```

#### Example: testing connection for application after running main.py  
![Implement your first API route!](https://github.com/bilan604/initiative/blob/main/static/use_api.png)  


## Public functionalities for this project:  

These endpoints don't require and id and are free to use (electricity not included), but there is a rate limiter for requests. Feel free to try them out or continue using as much as neccessary.  

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

## TLDR: what is this project?  
I made an API endpoint and am doing all my projects here but the code is not open source so I made a Flask API tutorial based off my project as an item to list in my project experiences. Also, free SERP API.

## TLDR: should I git clone?  
Looking for a fun/silly/challenging project to help you learn Python? Tired of circular dependencies? Itching to refactor even though you hate refactoring? Want to access existing code without another git init or docker compose? Simply need a flask template to quickstart something you had in mind? Need a production backend with architecture that can scale functionalities like AWS scales services?

If so, then this is the repo for you!

Git clone this project and run main.py so that you can host your website AND/OR API endpoint, using a simple, intuitive, atomic, and most importantly, scalable backend architecture to give your code an API route!

