# Initiative


```
def test_src(userId, operation, requestData):

    if type(requestData) != str:
        print("converting request data to json string")
        requestData = json.dumps(requestData)
    
    endpoint = "http://10.0.0.179:8000/api/"

    req_params = {
    "userId": userId,
    "operation": operation,
    "requestData": json.dumps(requestData)
    }

    response = requests.get(endpoint, params=req_params)
    
    return response.text
```
