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

