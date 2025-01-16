import os
import uuid
import json
from flask import Flask
from flask import session, request
from flask import redirect, render_template, url_for

from src.generic.loader import get_env_variable
from src.generic.loader import get_access_id
from src.generic.private_handler import runtime_environment_check
from src.generic.private_handler import get_job_applications

from src.generic.turtle import Turtle
from src.generic.encryption_manager import EncryptionManager
from src.generic.chat import MessageHandler

from src.generic.user import register as user_register
from src.generic.user import login as user_login
from src.generic.user import logout as user_logout
from src.generic.user import get_user_by_uuid
from src.generic.user import update_user_info
from src.generic.user import change_user_access_level
from src.generic.user import change_user_number_of_credits

from src.handler.router import add_routes  # adds 
from src.handler.requester import chatGPT35

from src.handler.sessions import get_operations_by_worker_id
from src.handler.sessions import  get_available_service_workers

# hanlding.py handles more handle-needing functions along with their args kwargs
# its basically an extra layer where functions are imported into the handler
# and wrapped around an error handling function taking (id, data) before being
# imported again here
from src.handling import test
from src.handling import get
from src.handling import google_search
from src.handling import google_search_pages
from src.handling import get_search_result_urls
from src.handling import prompt_autoauto
from src.handling import ask_openai
from src.handling import ask_GPT35, ask_GPT4
from src.handling import get_notefinder
from src.handling import add_notefinder
from src.handling import update_notefinder
from src.handling import create_notefinder
from src.handling import load_notefinder
from src.handling import query_notefinder
from src.handling import update_access
from src.handling import get_questions
from src.handling import get_product_url
from src.handling import get_product_urls

from src.handling import add_service_worker
from src.handling import remove_service_worker
from src.handling import create_session
from src.handling import delete_session
from src.handling import add_operation
from src.handling import add_application
from src.handling import add_row_to_sheet
from src.handling import api_file
from src.handling import btc_price
from src.handling import btc_usd_price


# These next two lines of imports should ideally pass through hsrc.anding
from src.generic.image_extraction import extract_text_from_image, get_data_from_extracted_text
from src.handler.sheets_orders import update_sheet_with_data


# DEVELOPMENT used to be a bool in .env but now is determined by the url after app runs
DEVELOPMENT = get_env_variable('DEVELOPMENT')

MESSAGE_HANDLER = MessageHandler(DEVELOPMENT)


app = Flask(__name__)

app.secret_key = get_env_variable("APP_SECRET_KEY")
app.config['SESSION_COOKIE_SECURE'] = False

# Define the upload folder (where uploaded screenshots will be stored)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = add_routes(app)


operationFunctionsMap = {
    "test": test,

    "get": get,

    "api_file": api_file,

    "ask_GPT35": ask_GPT35, # error
    "ask_GPT4": ask_GPT4,
    "btc_price": btc_price,
    "btc_usd_price": btc_usd_price,
    
    "prompt_autoauto": prompt_autoauto,
    "ask_openai": ask_openai,

    "google_search": google_search,
    "get_search_result_urls": get_search_result_urls,
    "google_search_pages": google_search_pages,
    "get_n_search_results": google_search_pages,

    "get_questions": get_questions,

    "get_notefinder": get_notefinder,
    "add_notefinder": add_notefinder,
    "update_notefinder": update_notefinder,
    "create_notefinder": create_notefinder,
    "load_notefinder": load_notefinder,
    "query_notefinder": query_notefinder,
    "update_access": update_access,

    # Adds a row to a google sheet
    # data{sheet_name: str, data: dict}
    "add_row_to_sheet": add_row_to_sheet,
    
    # data{prompt: str}
    #"generate_image": generate_image,

    "get_product_url": get_product_url,
    "get_product_urls": get_product_urls,

    "add_service_worker": add_service_worker,
    "remove_service_worker": remove_service_worker,
    "create_session": create_session,
    "delete_session": delete_session,
    "add_operation": add_operation,
    "add_application": add_application,
}

turtle = Turtle()
turtle.limits = {
    'get': 2,
    'ask_GPT35': 10,
    'ask_GPT4': 10,
    'ask_openai': 10,
    'prompt_autoauto': 30,
    'google_search': 1,
    'get_search_result_urls': 1,
    'google_search_pages': 1,
    'get_n_search_results': 1
}

em = EncryptionManager()


def handle_request_params(id, operation, request_data):
    global turtle
    global operationFunctionsMap

    if not turtle.canOperate(operation):
        rem = turtle.getRemaining(operation)
        return "Cooldown: "+ str(rem) + " seconds remaining"
    
    if operation not in operationFunctionsMap:
        return "operation not in operationFunctionsMap"
    resp = operationFunctionsMap[operation](id, request_data)

    # update the turtle!
    turtle.updateOperation(operation)
    
    return resp

def handle(request):
    global turtle
    if not turtle.can():
        return "Cooldown: 1 second remaining"
    
    try:
        data = request.get_json()
        id = data.get("id", None)
        if id == None:
            return "Parameter: 'id' not specified"
        operation = data.get("operation", None)
        if operation == None:
            return "Parameter: 'operation' not specified"
        request_data = data.get("request_data", None)
        if request_data == None:
            return "Parameter: 'request_data' not specified"
    except:
        id = request.args.get("id", None)
        if id == None:
            return "Parameter: 'id' not specified"
        operation = request.args.get("operation", None)
        if operation == None:
            return "Parameter: 'operation' not specified"
        request_data = request.args.get("request_data", None)
        if request_data == None:
            return "Parameter: 'request_data' not specified"
        request_data = json.loads(request_data)

    if DEVELOPMENT == 'TRUE': print("id:", id)
    if DEVELOPMENT == 'TRUE': print("operation:", operation)
    if DEVELOPMENT == 'TRUE': print("request_data:", request_data)

    resp = handle_request_params(id, operation, request_data)

    # update the turtle!
    turtle.update()
    
    return resp


@app.route("/admin/", methods=["GET", "POST"])
def admin():
    # First, check whether they can access the page.
    curr_uuid = session.get("uuid", -1)
    if curr_uuid == -1:
        return render_template('navigate.html', message="Please login as admin to access the admin panel.")
    user = get_user_by_uuid(curr_uuid)
    if user == None:
        return render_template('navigate.html', message="Could not find user for this session. Please login again as admin to access the admin panel.")
    
    access_level = user.user_info["ACCOUNT_TYPE"]
    if access_level != "ADMIN":
        return render_template('navigate.html', message="Please login as admin to access the admin panel.")

    # Handle get and post requests.
    if request.method == "GET":
        return render_template('admin.html', message="You are logged in as ADMIN.")
    elif request.method == "POST":
        button_label = request.form['button_label']
        
        if button_label == "Set Access Level":
            access_level_username = request.form['access_level_username']
            access_level = request.form['access_level']
            if user.username == access_level_username:
                message = "You can not change your own access level."
            else:
                message = change_user_access_level(access_level_username, access_level)
            return render_template('admin.html', message=message)
        
        elif button_label == "Set Credits":
            credits_username = request.form['credits_username']
            credit_count = request.form['credit_count']
            if type(credit_count) == str:
                try:
                    credit_count = int(credit_count)
                except:
                    return render_template('admin.html', message="Invalid Credit Count Input Provided.")
            
            # Too many credits who tf is trying to do this?
            if credit_count  > 1_000_000:
                return render_template('admin.html', message="Changing credit count to such is not yet implemented.")
            
            message = change_user_number_of_credits(credits_username, credit_count)
        
            return render_template('admin.html', message=message)
    else:
        return "Request Method Not Supported"

@app.route("/messages/", methods=["POST"])
def messages():
    global MESSAGE_HANDLER
    user_input = request.form.get('input', "")
    curr_uuid = session.get("uuid", -1)
    if curr_uuid == -1:
        if DEVELOPMENT == 'TRUE': print("Current uuid was -1")

    if user_input == "":
        is_first_load = request.form.get('isFirstLoad', "")
        uuid_key = str(curr_uuid)    
        if is_first_load == "TRUE":
            existing_messages = MESSAGE_HANDLER.get_chat(uuid_key)
            if existing_messages:
                return json.dumps(existing_messages)
            else:
                MESSAGE_HANDLER.create_empty_chat(uuid_key)
                return json.dumps(MESSAGE_HANDLER.get_chat(uuid_key))
        else:
            # accidental spaces should be handled in the chat class
            MESSAGE_HANDLER.create_empty_chat(uuid_key)
            return json.dumps(MESSAGE_HANDLER.get_chat(uuid_key))

    else:
        # add user message to chat so that it is included in the context window when calling chatGPT35
        uuid_key = str(curr_uuid)
        MESSAGE_HANDLER.add_chat_message(uuid_key, user_input)

        messages = MESSAGE_HANDLER.get_nonhtml_chat(uuid_key)
        ai_response = chatGPT35(messages)

        MESSAGE_HANDLER.add_chat_message(uuid_key, ai_response)
        #Hi, was it Adam or Eve that bit the apple in the Bible?
        page_messages = MESSAGE_HANDLER.get_chat(uuid_key)
        return json.dumps(page_messages)

@app.route("/chat/", methods=["GET", "POST"])
def chat():
    global MESSAGE_HANDLER
    if request.method == "GET":
        curr_uuid = session.get("uuid", -1)
        if curr_uuid == -1:
            #session['uuid'] = uuid.uuid4()
            return "Please Login first."
            
        return render_template("chat.html")
    
    
    if DEVELOPMENT == 'TRUE': print("Code should not have reached here!")
    return json.dumps(["Error, wrong type of request was made"])

@app.route("/navigate/", methods=["GET"])
def navigate():
    if request.method == "POST":
        nav_to = request.form['nav_to']
        if DEVELOPMENT == 'TRUE': print("-----> NAV TO ACTUALLY TRIGGERS?")
        if DEVELOPMENT == 'TRUE': print("nav_to:", nav_to)
        if nav_to:
            if "navigate" in nav_to:
                return redirect(f"/{nav_to}", message= "plc")
            return redirect(f"/{nav_to}")

            #return render_template(f'{nav_to}.html', message="plc")
    else:
        message = ""
        message_set = False

        curr_uuid = session.get("uuid", -1)
        user = None

        if curr_uuid == -1:
            user = get_user_by_uuid(curr_uuid)
        if user != None:
            # recently_applied_jobs is the entire matix with username = username
            recently_applied_jobs = get_job_applications(user.username)
            recently_applied_jobs = recently_applied_jobs[min(len(recently_applied_jobs), 30):]
            
            applications = []
            for app in recently_applied_jobs:
                if str(app[3]) != "nan" and str(app[4]) != "nan":
                    application_entry = app[4] + ": " + app[3]
                    applications.append(application_entry)
            if DEVELOPMENT == 'TRUE': print("applications:", applications)
            
            if recently_applied_jobs and not message_set:
                message = "Recently Appliced to Jobs:\n" + \
                    "\n".join(["<div>" + app + "</div>\n" for app in applications])
                message_set = True
            else:
                message = ""
                message_set = True
        
        return render_template('navigate.html', message=message)


@app.route("/update/", methods=["GET", "POST"])
def update():
    if request.method == "POST":
        curr_uuid = session.get("uuid", -1)
        user = None

        if curr_uuid == -1:
            return "Please Login"

        user = get_user_by_uuid(curr_uuid)
        if user == None:
            return f"Could not find user given session id {str(curr_uuid)}."
        
        update_user_info(user, request.form)
        return render_template('navigate.html', message="Your information has been updated.")
    else:
        # Check if the person is logged in
        curr_uuid = session.get("uuid", -1)
        if curr_uuid == -1:
            return "Please login."
            
        user = get_user_by_uuid(curr_uuid)
        if DEVELOPMENT == 'TRUE': print("IF USER NOT NONE THEN OK!\n--------->\n")
        if DEVELOPMENT == 'TRUE': print(user)
        return render_template('update.html')
    

@app.route("/applications/", methods=["GET", "POST"])
def applications():
    curr_uuid = session.get('uuid', -1)
    if curr_uuid == -1:
        return render_template('navigate.html', message="Please log in first to view applications.")
    
    if request.method == "GET":
        return render_template('applications.html')
    elif request.method == "POST":
        
    
        number_to_load = request.form["number_to_load"]
        # it is indeed passed as a string
        if type(number_to_load) == str:
            number_to_load = int(number_to_load)
        
        user = get_user_by_uuid(curr_uuid)
        if user == None:
            applications = []
        else:
            applications = get_job_applications(user.username)
        
        total_applications = len(applications)
        applications = applications[::-1]
        applications = applications[:min(len(applications), number_to_load)]
        
        def shave_urls(applications):
            # may end less than 50 due to broken links?
            # Would be another bug tho?
            new = []
            for i in range(len(applications)):
                url = applications[i][5]
                idx = url.find('currentJobId=')
                if idx == -1:
                    continue
                
                for j in range(idx+len('currentJobId='), len(url)):
                    if url[j] == "&":
                        applications[i][5] = url[:j]
                        break
                new.append(applications[i])
            return new

        def reduce_columns(applications):
            new = []
            for app in applications:
                if any([str(app[i]).lower() == 'nan' or not app[i] for i in (1,2,3,4,5)]):
                    continue
                jid = int(app[4])
                desc = app[3]
                url = app[5]
                time = app[7]
                new.append([jid, desc, url, time])
            return new
        
        applications = shave_urls(applications)
        applications = reduce_columns(applications)
        application_data = [total_applications, applications]
        return json.dumps(application_data)

    else:
        return "Request method not supported."


@app.route("/apply/", methods=["GET", "POST"])
def apply():
    if request.method == "GET":
        return render_template('apply.html')
    
    if request.method == "POST":
        # 1. Handle post requests from service workers
        session_operation = request.form["session_operation"]  # this was set by mannually passing a dict with the session operation parameter, instead of post html forms' built-in posts
        if session_operation == 'Find Active Service Worker':
            sw_names = get_available_service_workers()
            if not sw_names:
                return ''
            return sw_names[0]


        # 2. handle post requests from users
        curr_uuid = session.get("uuid", -1)
        if DEVELOPMENT == 'TRUE': print("\nAPPLY CURR_UUID:", curr_uuid)
        if curr_uuid == -1:
            return render_template("navigate.html", message="Please login first.")
        
        user = get_user_by_uuid(curr_uuid)
        if DEVELOPMENT == 'TRUE': print("apply() user_by_ip() user:", user)
        if user == None:
            return render_template("navigate.html", message="Please login first.")
        
        # Check if the user has enough credits
        if str(user.user_info["CREDITS"]).lower() == "nan" or user.user_info["CREDITS"] <= 0:
            if str(user.user_info["CREDITS"]).lower() == "nan":
                print("Nan user credit spotted")
            return render_template("navigate.html", message="You are out of credits.")

        session_operation = request.form["session_operation"]
        # should check login
        if session_operation == "Create Session":
            service_worker = request.form["service_worker"]
            required_fields = ['LINKEDIN_USERNAME', 'LINKEDIN_PASSWORD', 'RESUME']
            
            if any([user.user_info[rf] is None for rf in required_fields]):
                return f"User {user.username} has not provided linkedin email, password, or resume yet."
            
            LINKEDIN_USERNAME = user.user_info['LINKEDIN_USERNAME']
            LINKEDIN_PASSWORD = user.user_info['LINKEDIN_PASSWORD']
            ADDRESS = user.user_info['ADDRESS']
            SCHOOLS = user.user_info['SCHOOLS']
            RESUME = user.user_info['RESUME']
            if DEVELOPMENT == 'TRUE': print(LINKEDIN_USERNAME)
            if DEVELOPMENT == 'TRUE': print(ADDRESS)
            if DEVELOPMENT == 'TRUE': print(SCHOOLS)
            if DEVELOPMENT == 'TRUE': print(RESUME)
            user.user_info["SERVICE_WORKER"] = service_worker
            from src.generic.user import DATAHANDLER
            DATAHANDLER.update_user(user)

            data = {
                'worker_id': service_worker,
                'session_operation': 'session_start',
                'LINKEDIN_EMAIL': em.encrypt_string(LINKEDIN_USERNAME),
                'LINKEDIN_PASSWORD':  em.encrypt_string(LINKEDIN_PASSWORD),
                'city':  em.encrypt_string(ADDRESS),
                'schools': json.dumps(SCHOOLS),
                'resume': RESUME
            }
            resp = add_operation(user.username, data)
            return render_template("navigate.html", message=resp)
        if session_operation == "Session Load":
            if user.user_info["SERVICE_WORKER"] == '':
                return "No service worker assigned."
            
            search_term = request.form["search_term"]
            location = request.form["location"]
            pages = int(request.form["pages"])

            data = {
                'worker_id': user.user_info["SERVICE_WORKER"],
                'session_operation': 'session_load',
                'search_term': search_term,
                'location': location,
                'pages': pages
            }
            resp = add_operation(user.username, data)
            return render_template("navigate.html", message=resp)
        if session_operation == "Session Apply":
            if user.user_info["SERVICE_WORKER"] == '' or not user.user_info["SERVICE_WORKER"]:
                return "No service worker assigned."
            data = {
                'worker_id': user.user_info["SERVICE_WORKER"],
                'session_operation': 'session_apply',
            }
            resp = add_operation(user.username, data)
            return render_template("navigate.html", message=resp)
        if session_operation == "Load And Apply":
            if user.user_info["SERVICE_WORKER"] == '' or not user.user_info["SERVICE_WORKER"]:
                return "No service worker assigned."
            
            search_term = request.form["search_term"]
            location = request.form["location"]
            pages = int(request.form["pages"])
            if DEVELOPMENT == 'TRUE': print(search_term)
            if DEVELOPMENT == 'TRUE': print(location)
            if DEVELOPMENT == 'TRUE': print(pages)
            data_load = {
                'worker_id': user.user_info["SERVICE_WORKER"],
                'session_operation': 'session_load',
                'search_term': search_term,
                'location': location,
                'pages': pages
            }
            data_apply = {
                'worker_id': user.user_info["SERVICE_WORKER"],
                'session_operation': 'session_apply'
            }
            resp_load = add_operation(user.username, data_load)
            if DEVELOPMENT == 'TRUE': print("resp_load:", resp_load)
            resp_apply = add_operation(user.username, data_apply)
            if DEVELOPMENT == 'TRUE': print("resp_apply:", resp_apply)
            return render_template("navigate.html", message=resp_apply)
        return render_template('apply.html')  
    return "Request method not supported"


@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # bool, string
        register_attempt_success, register_attemp_message = user_register(username, password)
        return render_template('navigate.html', message=register_attemp_message)
        
    return "Request method not supported"


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        curr_uuid = session.get("uuid", -1)
        if curr_uuid == -1:
            # update session id
            new_uuid = uuid.uuid4()
            session["uuid"] = new_uuid
            logged_in = user_login(username, password, new_uuid)
            return render_template('navigate.html', message=logged_in)
        else:
            logged_in = user_login(username, password, curr_uuid)
            return render_template('navigate.html', message=logged_in)

    return "Request method not supported"

@app.route("/logout/", methods=["GET"])
def logout():
    if request.method != "GET":
        return "Request Method Not Allowed."
    
    curr_uuid = session.get("uuid", -1)
    if curr_uuid != -1:
        user_logout(curr_uuid)
        session.pop("uuid", None)
        return render_template('navigate.html', message="Successfully Logged Out.")
    
    return render_template('navigate.html', message="You need to log in first before logging out.")


@app.route('/sessions/<worker_id>', methods=['GET', 'POST'])
def sessions(worker_id):
    operations = get_operations_by_worker_id(worker_id)
    # pythonanywhere doesn't like returning raw jsons
    operations_json = json.dumps(operations)
    return operations_json
        

@app.route("/api/", methods=("GET", "POST"))
def api():
    if DEVELOPMENT:
        if DEVELOPMENT == 'TRUE': print("/api/ route called:")

    if request.method == "GET":
        return json.dumps({
            "message": "The format for a get response from API"
        })

    if request.method == "POST":
        response = handle(request)
        api_response = {
            "message": response
        }
        return json.dumps(api_response)

    return "None"


@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == "GET":
        return render_template('upload.html')

    if 'file' not in request.files:
        print("returning request.url:", request.url)
        return redirect(request.url)
    
    file = request.files['file']

    if file.filename == '':
        print("returning request.url:", request.url)
        return redirect(request.url)

    if file:
        # Save the uploaded file to the upload folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        ####
        image_path = file.filename
        print("image_path:", image_path, " (from file.filename)")
        image_path = f"uploads/{image_path}"

        extracted_text = extract_text_from_image(image_path)
        print("extracted_text:")
        print(extracted_text)

        data = get_data_from_extracted_text(extracted_text)
        print("data:")
        print(data)
        
        update_sheet_with_data(data)
        
        return 'File uploaded successfully!'

    return 'Error uploading file.'


@app.route("/", methods=("GET", "POST"))
def hello_world():
    global DEVELOPMENT
    if '127.0.0' in request.host_url:
        DEVELOPMENT = 'True'
    else:
        DEVELOPMENT = 'False'
    print("DEVELOPMENT variable set to " + DEVELOPMENT)

    response = ""
    if request.method == "POST":
        query = request.form['query']
        if DEVELOPMENT == 'TRUE': print("Query: ", query)
        if query and len(query) > 0:
            response = handle_request_params('', 'prompt_autoauto', {
                "query": query
            })
        return render_template('index.html', prompt_response=response)
    
    return render_template('index.html', prompt_response=response)


# a function to run this app from main.py
def run_app():
    os.chdir(os.getcwd())
    runtime_environment_check()
    app.run()


