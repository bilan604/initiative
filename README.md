# Take Initiative! (API Documentation, Tutorial, and Template)
@Author: Xing Yang Lan

## Intro:
I started this project because I realized that a lot of the code I was writting for unrelated personal projects, for fun, and for assigned projects were similar in nature, but not concrete enough or important enough to make a Github repository for. 

Realizing that this could be overcome by placing the repetitive functionalities from different repositories together in a single repository, I decided to make an API and aggregate isolated functionalities from old projects into this single project, but instead of making seperate API routes for them, just giving each functionality a name for the operation that it performs.

Now, the flask server (url below) hosts an API endpoint for me and my friends' projects - allowing functionalities to be accessed without git cloning or pip installations in remote environments.

[Landing Page](http://bilan604.pythonanywhere.com)  

NOTE: This repository isn't the actual repository for the url above. Since I added the code for most of the functionalities in the .gitignore, but wanted to make the repository public as well, I have changed this repository so that it is basically a flask tutorial to help people get into Python/Flask. (Its more exciting than learning for loops! :D)

## Installation
1. Navigate the folder that you want the project to be in.
2. Git clone this repository and navigate to the folder.
```
git clone https://github.com/bilan604/initiative.git
cd ./initiative
```
3. Install the requirements
```
pip install -r requirements.txt
```

## Running  
Git Bash
```
python main.py
```
Running main.py locally automatically sets the environment variable DEVELOPMENT to true. The variable is used for console logs and is ONLY true when the app is run from the file "__main__.py".

## Troubleshooting  
If you encounter any errors installing requirements from ```requirements.txt``` just use pip to install them mannually like ```pip install beautifulsoup4```.

The above issue may be caused by not having a high enough version of Python. You can check your version using:
```
python --version
```

Try upgrading pip:
```
pip install --upgrade pip
```

If you have multiple versions, make sure that the Python interpreter is using the right version of Python (ctrl+shift+p if you are using vscode).

You can also specify a specific version of Python if you have multiple versions of Python in git bash like ```python3.11 -m pip install beautifulsoup4``` . If you do this, please note that each version of Python you have installed has its own version of pip!.
```
python3.11 -m pip install --upgrade pip
```

## Post Request Format  

The /api/ endpoint takes an id, the desired functionality (similar to specifying 'Content-Type' in the headers for a post request, but for the route itself), and the request_data which is a json string containing the parameters for the function. (This is literally the chunk of code I copy to use it)

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


## Private functionalities for this project:  

#### Using Selenium and GPT-4 to answer questions online:

https://github.com/bilan604/initiative/assets/77251582/d45149ed-a9df-414f-b8e8-03d1bca8f70b

Witness the browser answering it's own questions! If you have questions about the details, or want to use this endpoint as well, just ask :)

## Public functionalities for this project:  

These endpoints don't require and id and are free to use (electricity not included). Feel free to try them out or continue using them, they're free because there's a rate limiter on operations.  

#### SERP API:

Returns the first page of urls for a search result.

```
    pars = {
        'id': '',
        'operation': 'get_search_result_urls',
        'request_data': json.dumps({
            'query': 'string: the search query',
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
            'query': 'string: the search query',
            'n': integer: desired number of results
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
Looking for a fun/silly/challenging project to help you learn Python? Tired of circular dependencies? Hate refactoring and itching to refactor things? Want to access existing code without another git init or docker compose? Simply need a flask template to quickstart something you had in mind? Need a production backend with architecture that can scale functionalities like AWS scales services?

If so, then this is the repo for you!

Git clone this project and run main.py so that you can host your website AND/OR API endpoint, using a simple, intuitive, atomic, and most importantly, scalable backend architecture to give your code an API route!

