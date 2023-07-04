# Initiative Endpoint  

This repository is the remote head for aggregating code into one place. If you are git cloning this, you will have to replace the placeholders. I can not add all of the code to a public repo.  

However, if git cloning, you will just need to replace the handler file with placeholder functions. This repository can be used as a template for your own endpoint.  

## 1. Autofill Chrome Extension:  
1. Git clone this repository.  
2. Install the dependencies.  
3. Open the chome-extension and go to bachground.js. Fill in your GPT-4 API key on line 111.  
4. run `python main.py` in git bash to start the server.  
5. Go to Google Chrome -> More Tools -> Extensions.  
6. Toggle developer mode to on (top right).  
7. Click load unpacked (top left), and select the folder 'chrome-extension'.  
8. Toggle the extension to on if it is not on by default.  
9. Click 'background page' and go to console to see the console logs and verify it is working.  

#### Ping:  
Check the landing page is up:
Visit http://10.0.0.179:8000 (localhost)  

#### Use the API endpoint:  
```
import json
import requests


def api_request(userId, operation, requestData):
    # Specify an endpoint in main
    endpoint = "http://10.0.0.179:8000/api/"

    req_params = {
        "userId": userId,
        "operation": operation,
        "requestData": json.dumps(requestData)
    }

    response = requests.get(endpoint, params=req_params)
    
    return response.text


```
