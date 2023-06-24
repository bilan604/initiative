# Initiative

This repository is the remote head for the backend of the initiative project, an API endpoint to aggregate some of the code I have written over the years.  

This repo will not work when git cloned, because I am adding most of the folders to the .gitignore, but you can feel free to use it as an amazing template for developing an atomic, scalable, and structured Flask Endpoint.  

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
