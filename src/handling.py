from src.handler.loader import get_handler_env


DEVELOPMENT = False


if get_handler_env() == 'True':
    DEVELOPMENT = True

def test(id, data):
    if DEVELOPMENT == True:
        print(data)
    return True

def your_api_functionality(id, data):
    def isValidForFunctionality(id): 
        # check the requests!
        return True
    def do_functionality(input_argument: str) -> str:
        # grab a function!
        # This backend supports the integration of functions
        # with input arguments of any datatype
        # EXCEPT strings containing characters that can not be json encoded/decoded

        # But I have a workaround. DM me if you encounter a similar problem.
        api_response = "Your API is working! " + input_argument
        return api_response

    if not isValidForFunctionality(id):
        return "Invalid ID"
    if "arg1" not in data:
        return "Please specify the input argument"
    
    arg1 = data['arg1']
    resp = do_functionality(arg1)
    return resp
    

