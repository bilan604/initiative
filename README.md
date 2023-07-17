# Initiative Endpoint  

This repository is the remote head for aggregating code into one place. If you are git cloning this, you will have to replace the placeholders. I can not add all of the code to a public repo.  

#### Ping:  
Check the landing page is up:
Visit http://10.0.0.179:8000 (localhost)  

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
