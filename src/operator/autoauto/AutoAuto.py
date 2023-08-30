import time
import string

from src.operator.autoauto.api import *
from src.operator.autoauto.parsing import *
from src.operator.autoauto.google_search import *


def strip_args(func, args):
    valid = string.ascii_letters + "0123456789"
    args = list(args)
    while args and args[-1] not in valid:
        args.pop()
    args = args[::-1]
    while args and args[-1] not in valid:
        args.pop()
    args = args[::-1]
    args = "".join(args)
    if func == "__SUBTASKS__":
        args = [arg.strip() for arg in args.split("\n") if arg.strip()]
        return args
    return args

def get_function(agent, resp):
    for func in agent.functions:
        if func in resp:
            return func
    return None

def get_function_args(agent, resp):
    func = get_function(agent, resp)
    if func == None:
        return None
    
    args = "".join(resp.split(func)[1:])
    args = strip_args(func, args)

    return args


def finalize_response(agent, subtask_objective, previous):

    if subtask_objective == agent.objective:
        description = "Your MAIN_OBJECTIVE:"
    else:
        description = "Your SUBTASK_OBJECTIVE:"
    
    prompt = \
    f"""\
{format(description, subtask_objective)}
{format("Your Previous Response", previous)}

This is the final prompt in the prompt chain. Take the instructions in you OBJECTIVE and \
finalize the formatting / aggregate the information available to provide your final response.

Your response to this verdict will be the final response for to the OBJECTIVE provided above."""
    resp = get_prompt_response(agent, prompt)
    return resp



#######################################
def handle_subtasks(agent, subtasks):
    ########## 0
    return agent.handle_subtasks(subtasks, 0, 0)

def visit(agent, url):
    return get_content_by_url(url, agent.objective)

def get_prompt_response(agent, prompt):
    resp = get_gpt4_result(prompt)
    
    agent.prompts.append(prompt)
    agent.responses.append(resp)
    return resp

def get_search_urls(agent, query):
    return get_search_results(query)

def get_search_results_with_agent(agent, query):
    return get_search_query_content(query)

def do_execute(code):
    global output_variable, output_error
    output_variable = None
    output_error = None
    try:    
        ##########
        # asign last variable to output variables
        code = "global output_variable, output_error\n" + code
        code = [l.strip() for l in code.split("\n") if l.strip()]
        if "print" in code[-1]:
            code[-1] = code[-1].replace("print", "", code[-1]) + "[0]"
        
        code[-1] = f"output_variable = {code[-1]}"
        code = "\n".join(code)
        
        print("!!!!!!!!!!!!!!!!!!!!!!!!! executing code:")
        print(code)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!")

        exec(code)
        
        return output_variable, output_error

    except Exception as e:
        print("Error:", e)
        return output_variable, e

def execute(agent, code):
    code_output, error = do_execute(code)
    if code_output == None:
        return f"""\
Error:
```
{error}
```
occured when executing code:
```
{code}
```
"""
    
    return f"""\
Executed Code:
{code}

Code Output:
{code_output}\
"""



######################
def chain(agent, objective, subtask_objective, previous_response, prompt_depth):
    inside_subtask = ""
    if subtask_objective != "":
        inside_subtask = \
        f"""\
You are currently inside a subtask. Your subtask objective is to forward your MAIN_OBJECTIVE given your previous response.\
{format("Your SUBTASK_OBJECTIVE", subtask_objective)}
"""

    s = \
    f"""\
Your task is to complete your MAIN_OBJECTIVE given the objective.

{format("Your MAIN_OBJECTIVE", agent.objective)}
{inside_subtask}
{indent(format("Your SUBTASK_OBJECTIVE", subtask_objective))}
{indent(format("Your PREVIOUS_RESPONSE", previous_response))}
{indent(get_nonsubtask_outro(agent, objective, prompt_depth))}\
"""
    return s

# eval takes two args
def get_nonsubtask_outro(agent, objective, depth):
    s = \
    f"""\
You have the option to continue your chain of thought or do one of the following functionalities:
```
=>__SUBTASKS__: \
Creates a list of subtasks. Does this chain of thought multiple times basically.
=>__RETURN__: \
Returns your response to this prompt (as the result of) and immediately ends this chain of prompts. If you realized that the current subtask is not doable for example, you can exit early with an error response.
=>__SEARCH__: \
Gets content from the internet given a search query. Will be stored in your next prompt as the result of your previous prompt.
=>__GET_SEARCH_URLS__: Gets a list of urls for a given search query. Will be stored in your next prompt as the result of your previous prompt.
=>__VISIT__: \
Visits a url and returns the text content from the url. Will be stored in your next prompt as the result of your previous prompt.
=>__EXEC__: \
Executes a chunk of Python code. List the variable that you want passed to the next prompt on the last line of the code, by itself. The variable's value \
will be parsed and to a global variable.

i.e.:```\
code = \"\"\"
import numpy as np
arr = np.array([[0,1,2], [2,3,1]])

arr
\"\"\"
a,b=do_execute(code)
print(a)
print(b)```

=>__COMPLETE__: If you realize you have already completed your objective, respond with "__COMPLETE__:\n" followed immediately by your response to the objective. Conside the objective the prompt, and the text following "__COMPLETE__:\n" the response. \
i.e. "__COMPLETE__: A short, consice answer for the objective"
```
To select a functionality, respond in the format "__FUNCTIONALITY__:\n[the args for your functionality]".
Subtasks should be listed in the format: "__SUBTASKS__:\n1) description for subtask one\n2) description for subtask two\n" etc...

Alternatively you can choose none of the above and simply further your chain of though reasoning. Your response to this prompt will be included by default in your next prompt.


Do not forget the original objective. There are {depth} prompt(s) remaining in this chain of prompts, and a global upper bound of {agent.N**2} prompts (not including the prompts from parsing Google searches).\
"""
    return s


class AutoAuto(object):
    def __init__(self, objective="", N=5):
        self.objective = objective
        self.driver = None
        self.prompts = []
        self.responses = []
        self.N = N
        self.result = ""
        self.functions = {
            "__SUBTASKS__": handle_subtasks,
            "__RETURN__": get_prompt_response,
            "__SEARCH__": get_search_results_with_agent,
            "__GET_SEARCH_URLS__": get_search_urls,
            "__VISIT__": visit,
            "__EXEC__": execute
        }

    def handle_function(self, resp):
        """
        Checks if there is a function and handles it

        Returns outcome of operation
        """
        func = get_function(self, resp)
        if func == None:
            ##########    
            pass
        args = get_function_args(self, resp)

        if func == "__EXEC__":
            function_declrs = ["def exec", "def store", "def get_search_urls", "def get_prompt_response", "def visit", "os.chdir", "os.set", "os.", "subprocess.", "w+"]
            if any([fd in resp for fd in function_declrs]):
                return "Parsing Error"

        return self.functions[func](self, args)

    def handle_subtasks(self, subtasks, subtask_depth, prompt_depth):
        if self.result:
            return self.result
        
        # cache
        resp = ""
        responses = []
        for subtask in subtasks:
            resp = self.interpret_chain(subtask, resp, subtask_depth + 1, self.N)
            responses.append(resp)
        
        return finalize_response(self, self.objective, resp)

    def interpret_chain(self, subtask_objective, previous, subtask_depth, prompt_depth):
        # interpret_chain = self.chain
        if self.result:
            print("self.result base case triggered")
            return self.result
        
        # Here is where subtasks can be made
        if subtask_depth > 2:
            return "[Too many subtasks]"
        if prompt_depth == 0:
            return finalize_response(self, subtask_objective, previous)
        
        prompt = chain(self, self.objective, subtask_objective, previous, prompt_depth)
        #print("\nprompt::::::::::::::::::::::::::::::::::::::::::")
        #print(prompt)
        resp = get_prompt_response(self, prompt)
        #print("\nresp:____________________________________________")
        #print(resp)

        time.sleep(1)

        func, args = get_function(self, resp), get_function_args(self, resp)
        if func == "__RETURN__":
            return args
        if func == "__COMPLETE__":
            self.result = args
            return self.result
        if func == "__SUBTASKS__":
            subtasks = parse_subtasks(previous)
            return self.handle_subtasks(subtasks, subtask_depth, prompt_depth)

        if func != None or args != None:
            if not (func != None and args != None):
                print("\n++++++++++++++++++++++++++++++++Error", func,"++++++++++" , args)
                time.sleep(20)
            # instead of passing the response as the previous
            # for the next chain prompt
            # pass the mutation of the next prompt as the previous result
            new_previous = self.functions[func](self, args)
            return self.interpret_chain(subtask_objective, new_previous, subtask_depth, prompt_depth - 1)
                
        return self.interpret_chain(subtask_objective, resp, subtask_depth, prompt_depth - 1)

    def finalize_response(self, interpretation):
        return interpretation

    def complete_objective(self):
        # add more interpretations
        interpretation = self.interpret_chain("", "", 0, self.N)
        # handle last prompt, etc
        result = self.finalize_response(interpretation)
        self.result = result












