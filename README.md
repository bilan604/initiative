# python-server

A Python Flask Server and flask server template for aggregating parallel processes. By aggregating various functionalities into a backend which is hosted online, I can access my code accross devices, virtual envs, and repositories.  

Originally developed from the OpenAI quickstart tutorial, the updated ```flask_app.py``` and new ```handling.py``` files are an example / template backend python server demonstrating modular implementation of functionalities. By specifying the operation inside the request data, and the request data as well, a single function map allows for all requests to be handled in a single file, ```src/handling.py```, while the code for the functionalities can be added to a folder or file in src/operator or src/handler.

## View Most recent build running:  
[http://bilan604.pythonanywhere.com](Website)  


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

## Troubleshooting  
Check the python version
```
python --version
```

Upgrade pip. Older versions of packages can cause code to behave unexpectedly without warning.
```
pip install --upgrade pip
```

## Calling the API
```
# No id has to be specified to request the API as of now

def ping_autoauto():
    import requests
    URL = 'http://bilan604.pythonanywhere.com/api/'

    pars = {
        'id': '',
        'operation': 'prompt_autoauto',
        'request_data': json.dumps({
            'query': 'Ping'
        })
    }

    resp = requests.post(URL, params=pars)
    print(resp.text)
    return resp.text  # remember to json.loads()

ping_autoauto()
```

## Operations

Not all are going to be listed, because this is more of a personal API, but here are two of the more helpful ones.

1. prompt_autoauto: Prompts autoauto, like on the landing page . request_data takes ```query```. 
2. get_search_result_urls: Gets the urls from Google search results for a query. request_data takes ```query```. 

