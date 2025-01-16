# ProjectsAPI! (API Documentation, Tutorial, and Template)
@Author: Xing Yang Lan

## About:

This is the original repo for making a server & database to handle backend post requests as well as front-end navigation panels to monitor and control processes. 

For example, here is an instance of the server that I am hosting [link to server](http://bilan604.pythonanywhere.com) (Seperate Repository)

Some features of ProjectsAPI:  
1. Improves modularity by aggregating code from different projects.  
2. Increases the accessibility of code (i.e. Allowing headless VM instances to make post requests for updates).  
3. Allows headless VM instances to make updates via post requests to the website.  
4. Act as a control panel for active bots.  

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
Returns```
    {
    'price': '100253.231',
    'time': '2025-01-16T18:19:31+00:00'
    }'''

#### CURL Example:
```
curl -X POST "https://bilan604.pythonanywhere.com/api/" \
     -H "Content-Type: application/json" \
     -d '{ "id": "bilan604", "operation": "btc_price", "request_data": {"currency": "USD"}}'
```

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

3. Install the dependencies and run main.py.  

