# python-server

A Python Flask Server and flask server template for aggregating parrallel processes. By aggregating various functionalities into a backend which is hosted online, I can access my code accross devices, virtual envs, and repositories.  

Originally developed from the OpenAI quickstart tutorial, the updated ```flask_app.py``` and new ```handling.py``` files are an example / template backend python server demonstrating modular implementation of functionalities. By specifying the operation inside the request data, and the request data as well, a single function map allows for all requests to be handled in a single file, ```src/handling.py```, while the code for the functionalities can be added to a folder or file in src/operator or src/handler.

View Most recent build running:  
[Website](http://bilan604.pythonanywhere.com)  

View The Original Quickstart Tutorial Template:
[https://github.com/openai/openai-quickstart-python](OpenAI Python Quickstart Tutorial)


## Running the Server:
```
python main.py
```

## Running tests
```
python test.py
```

## Requirements
-git bash
-python version 3.11

Since most of the files are in the gitignore, running ```pip freeze > requirements.txt``` will install the dependencies present for the Flask template.
