# Initiative Endpoint  

This repository is the remote head for aggregating code into one place. If you are git cloning this, you will have to replace the files with placeholders. Most of the code will be added to the .gitignore, because it may or may not have been written for projects not pertaining to this endpoint itself.  

#### Ping:  
Check the landing page is up:
Visit http://10.0.0.179:8000

#### Use the API endpoint:  
```
def api_request(userId, operation, request_data):
    # Specify an endpoint in main
    endpoint = "http://10.0.0.179:8000/api/"

    req_params = {
        "id": userId,
        "operation": operation,
        "request_data": json.dumps(request_data)
    }

    response = requests.get(endpoint, params=req_params)
    print("\nresponse:", response)
    
    return json.loads(response.text)
```
