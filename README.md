# Initiative

Check the landing page is up:
http://10.0.0.179:8000

#### ToDo:  
1. Setup frontend  
2. Run on GCP or AWS  
3. Separate repo for the front-end  
4. Set Up Database, either Firebase or SQL depending on what is used to build the front-end  


```
def api_request(userId, operation, requestData):

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
