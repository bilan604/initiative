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
import json
import requests

def ping_autoauto():
    
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
    return resp.text  # remember to json.loads()! :)

ping_autoauto()
```

