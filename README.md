# Initiative Endpoint  

The main reason this exists is because I would prefer to use git for my personal projects to be able to access the code accross devices. For now, this is an local API endpoint that aggregates various operations and functionalities I have coded into one place. It includes functionalities such as finding questions and answering the questions with information I have stored, so that certain forms can be filled by providing a lambda function.

Note: Files required to run from a git clone may have been added to the gitignore.

## Running:
1. git clone this repo
2. install dependencies with pip or however you prefer. I use ```pip install [package_name]```
3. run main.py based on how you installed the dependencies. I run 
```
python main.py
```
in git bash

#### Pinging:  
<<<<<<< HEAD
The landing page is set as:  
http://10.0.0.179:8000  

Its a placeholder. Yo0u can use it to see if the endpoint is up.

#### Get requests to the API endpoint:  

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
    
    return json.loads(response.text)
```

Like:  
```
request_data = {
    "tablename": "input",
    "query": "How many years of Python programming experience do you have?"
}
response = api_request("bilan604", "search_datatable", request_data)

print(response)

"""
4
"""
```

Or (from tests/test_endpoint.py):  
```
request_data = {
    "src": easy_apply_src,
    "rule": 'lambda x: "class" in x and "jobs-easy-apply-form-section__grouping" in x["class"]'
}

response = api_request("bilan604", "get_extracted_questions", request_data)

for r in response:
    print("Question:", r["question"])

# Output:
"""
Question: How many years of work experience do you have with Data Pipelines?
Question: How many years of work experience do you have with Shell Scripting?
Question: How many years of work experience do you have with Python (Programming Language)?
Question: Do you have a U.S. Citizenship required to qualify for a DoD interim Secret (or higher) security clearance?
Question: Do you have at least 2+ years experience with any of the following: MATLAB, Embedded Multi-Threaded development, ARM microprocessors, or any deep learning, TensorFlow?
Question: Are you comfortable working in a hybrid setting?
Question: Are you comfortable commuting to this job's location?
"""
```
=======
http://bilan604.pythonanywhere.com/
>>>>>>> 2aa69a78a56d6659452f32bebe25a921cb9c1f07

