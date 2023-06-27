# Initiative  


This repository is the remote head for the backend of the initiative project, an API endpoint to aggregate some of the code I have written over the years.  

This repo will not work when git cloned, because I am adding most of the folders to the .gitignore, but you can feel free to use it as an amazing template for developing an atomic, scalable, and structured Flask Endpoint.  

## Usage:  
#### Ping:  
Check the landing page is up:
Visit http://10.0.0.179:8000

#### Use the API endpoint:  
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

#### My ToDos:  
1. Setup frontend  
2. Run on GCP or AWS  
3. Separate repo for the front-end  
4. Set Up Database, either Firebase or SQL depending on what is used to build the front-end  

