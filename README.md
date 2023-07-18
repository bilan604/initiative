# Initiative Endpoint  

This is a local API endpoint that aggregates various operations and functionalities I have coded into one place. It includes functionalities such as finding questions and answering the questions with information I have stored, so that certain forms can be filled by providing a lambda function.

## Running:  
```
python main.py
```

#### Pinging:  
The landing page is set as:  
http://10.0.0.179:8000  

Visit page in browser to see if the server is up.  

#### get requests to the API endpoint:  

Heres a function that handles it:  
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
