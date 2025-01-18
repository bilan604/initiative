# ProjectsAPI!  
@Author: Xing Yang Lan

## About:

This is the original repo for making a server & database to handle backend post requests as well as front-end navigation panels to monitor and control processes. 

For example, here is my projects website, hosting an instance of this server [link to Website](http://bilan604.pythonanywhere.com) (Seperate Repository)

Some features of ProjectsAPI:  
1. Improves modularity by aggregating code from different projects.  
2. Increases the accessibility of code (i.e. Allowing headless VM instances to make post requests for updates).  
3. Allows headless VM instances to make updates via post requests to the website.  
4. Act as a control panel for active bots.  

![PythonAnywhere Image](https://raw.githubusercontent.com/bilan604/initiative/main/assets/pythonanywhere.png)

## Examples:

The /api/ endpoint handles POST handles generic requests where different functionalities by taking:
```
"id": "[an optional identifier]"
"operation": "[name of operation]"
"request_data": "[a json string of the key word arguments]"
```

#### Python Example:
```
import json
import requests

def post_request(pars):
    resp = requests.post(f'https://bilan604.pythonanywhere.com/api/', params=pars).text
    return json.loads(resp)["message"]

pars = {
    "id": "bilan604",
    "operation": "btc_price",
    "request_data": json.dumps({
        "currency": "USD"
    })
}

print(post_request(pars))
```

response:
```
    {
    'price': '100253.231',
    'time': '2025-01-16T18:19:31+00:00'
    }
```

#### CURL Example:
```
curl -X POST "https://bilan604.pythonanywhere.com/api/" \
     -H "Content-Type: application/json" \
     -d '{ "id": "bilan604", "operation": "btc_price", "request_data": {"currency": "USD"}}'
```

![benjamin btd6](https://static.wikia.nocookie.net/b__/images/a/af/BenjaminPortrait.png/revision/latest/smart/width/400/height/225?cb=20190612025211&path-prefix=bloons)

## Forking the repo:  
1. Clone the project
```
git clone https://github.com/bilan604/initiative.git
cd ./initiative
```

2. Create and enter a virtual environment
```
python3 -m venv myenv
source myenv/bin/activate
```

3. Install the dependencies
```
pip freeze > requirements.txt
pip install -r requirements.txt
```

## Host a server on the web:  

1. Go to https://www.pythonanywhere.com/ and create a web app.

2. Open the bash console, switch to your user directory, and clone this repo.
```
cd /home/[username]/
git clone https://github.com/bilan604/initiative.git
```

3. Go to the control panel for the web app and edit the WSGI configuration file.
```
import os

os.chdir('/home/[username]/initiative')

from flask_app import app as application
```

4. Since most of the files in this repo are in the .gitignore, replace 'flask_app.py' with a base empty template to avoid import errors.
```
import os
from flask import Flask
from flask import session, request

app = Flask(__name__)

def handle(request):
    pass

@app.route("/api/", methods=("POST"))
def api():
    if request.method == "POST":
        response = handle(request)
        return json.dumps({
            "message": "The format for a get response from API"
        })
    return json.dumps({
            "message": "Request method not supported"
        })

@app.route("/", methods=("GET"))
def hello_world():
    if request.method == "GET":
        return "Hello World!"

def run_app():
    os.chdir(os.getcwd())
    app.run()
```


