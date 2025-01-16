import os
import json
import pandas as pd

from src.generic.encryption_manager import EncryptionManager
from src.generic.loader import get_env_variable

from src.generic.user import get_user_by_username


DEVELOPMENT = get_env_variable('DEVELOPMENT')

EM = EncryptionManager()


class Session(object):
    def __init__(self, user_id, worker_id, max_time: 120):
        self.user_id = user_id
        self.worker_id = worker_id
        self.max_time = max_time

    def to_row(self):
        return [self.user_id, self.worker_id, self.max_time]

# :( Was faster to not reconcile differing user classes.
class User:
    def __init__(self, username, access_level):
        self.username = username
        self.access_level = access_level

    def to_row(self):
        return [self.username, self.access_level]

class ServiceWorker:
    def __init__(self, name, users, operations):
        self.name = name
        self.users = users
        self.operations = operations
    
    def to_row(self):
        users_json = json.dumps(self.users)
        operations_json = json.dumps(self.operations)
        return [self.name, users_json, operations_json]


class USS(object):
    def __init__(self, DB_NAME):
        self.DB_NAME = DB_NAME
        self.cwd = os.getcwd()
        ###############
        self.path = ['src', 'generic', 'private_files'] #['src', 'generic', 'private_files']  ################
        self.separator = '\\'
        if "/" in os.getcwd():
            self.separator = "/"

        self.files = ['session_service_workers.csv', 'session_sessions.csv', 'session_users.csv']
        self.columns = {
            'session_users.csv': [],
            'session_sessions.csv': [],
            'session_service_workers.csv': []
        }
        self.initialize()

    def get_file_path(self, file_name):
        prefix = self.get_prefix()
        if prefix:
            file_path = prefix + self.separator + file_name
        else:
            file_path = file_name
        return file_path
    
    def check_file_empty(self, file_name):

        prefix = self.get_prefix()
        if prefix:
            file_path = prefix + self.separator + file_name
        else:
            file_path = file_name
        
        lines = []
        with open(file_path, 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            

        for line in lines:
            if line.strip():
                return False
        return True

    def __read_csv(self, path):
        df = pd.read_csv(path)
        if "Unnamed: 0" in df.columns:
            if DEVELOPMENT == 'TRUE': print("\n!!!!!!!!!!!!!!!!!!!\nDATA INTEGRITY ERROR:\nUNNAMED: 0 in df.columns")
            df = df.drop(columns=["Unnamed: 0"])
        return df
    
    def get_prefix(self):
        if not self.cwd.strip():
            prefix = self.separator.join(self.path)
        else:
            prefix = self.cwd + self.separator + self.separator.join(self.path)
        return prefix
    
    def read_csv(self, file_name):
        prefix = self.get_prefix()
        if prefix:
            file_path = prefix + self.separator + file_name
        else:
            file_path = file_name
        
        df = self.__read_csv(file_path)
        return df

    def to_dict(self, df):
        dd = dict(df)
        for k in dd:
            dd[k] = list(dd[k])
        return dd

    def load_dict(self, file_name):
        df = self.read_csv(file_name)
        dd = self.to_dict(df)
        return dd

    # Private Method
    def load_mtx(self, file_name) -> list[list]:
        file_is_empty = self.check_file_empty(file_name)
        if file_is_empty:
            raise Exception("Attempted to load empty file:")

        df = self.read_csv(file_name)
        mtx = []
        for i in range(len(df)):
            row = []
            
            for j in range(len(self.columns[file_name])):
                row.append(df.iloc[i][j])
            mtx.append(row)
        return mtx

    def initialize(self):
        self.cwd
        if DEVELOPMENT == 'TRUE': print("self.cwd:---->")
        if DEVELOPMENT == 'TRUE': print(self.cwd)
        if '\\' not in self.cwd:
            self.separator = '/'
        prefix = self.get_prefix()
        for file in self.files:
            empty = self.check_file_empty(file)
            #raise Exception(f"{file_path} could not be accessed")
            if not empty:
                df = self.read_csv(file)
        
        # Mandatory override the hardcoded column names for each df
        for file_name in self.files:
            file_is_empty = self.check_file_empty(file_name)
            if file_is_empty:
                raise Exception("Attempted to load empty file:")
            df = self.read_csv(file_name)
            self.columns[file_name] = list(df.columns)
    
    def save_dict(self, file_name, dd):
        df = pd.DataFrame(dd)
        file_path = self.get_file_path(file_name)
        if DEVELOPMENT == 'TRUE': print("save_dict() file path:", file_path)
        df.to_csv(file_path, index=False)
    
    def load_users(self):
        dd = self.load_dict('session_users.csv')
        USERS = []
        ddk = list(dd.keys())
        for i in range(len(dd[ddk[0]])):
            user = User(dd[ddk[0]][i], dd[ddk[1]][i])
            USERS.append(user)
        return USERS

    def load_sessions(self):
        dd = self.load_dict('session_sessions.csv')
        SESSIONS = []
        ddk = list(dd.keys())
        for i in range(len(dd[ddk[0]])):
            user_id = dd[ddk[0]][i]
            worker_id = dd[ddk[1]][i]
            max_time = dd[ddk[2]][i]
            if not max_time or str(max_time).lower() == 'nan' or type(max_time) != int:
                max_time = 0
            
            session = Session(user_id, worker_id, max_time)
            SESSIONS.append(session)
        return SESSIONS

    def load_service_workers(self):
        dd = self.load_dict('session_service_workers.csv')
        SERVICE_WORKERS = []
        ddk = list(dd.keys())
        for i in range(len(dd[ddk[0]])):
            name = dd[ddk[0]][i]
            users_json = dd[ddk[1]][i]
            ####
            # should be using list of user ids, not user objects. (Update as of 03/04/2024)
            users = json.loads(users_json) ####
            operations_json = dd[ddk[2]][i]
            operations = json.loads(operations_json)
            service_worker = ServiceWorker(name, users, operations)
            SERVICE_WORKERS.append(service_worker)
        return SERVICE_WORKERS

    def get_user(self, id):
        USERS = self.load_users()
        for u in USERS:
            if u.username == id:
                return u
        return None    

    def get_service_worker(self, id):
        SERVICE_WORKERS = self.load_service_workers()
        for sw in SERVICE_WORKERS:
            if sw.name == id:
                return sw
        return None
    
    def get_session(self, user_id, worker_id):
        # Not used currently but could be helpful for checking max time
        SESSIONS = self.load_sessions()
        for session in SESSIONS:
            if session.user_id == user_id and session.worker_id == worker_id:
                return session
        return None
    
    def update_users(self, USERS):
        ddk = self.columns['session_users.csv']
        UPDATED_USERS = {k: [] for k in ddk}
        for i in range(len(USERS)):
            for j in range(len(ddk)):
                user_row = USERS[i].to_row()
                UPDATED_USERS[ddk[j]].append(user_row[j])
        self.save_dict('session_users.csv', UPDATED_USERS)

    def update_service_workers(self, SERVICE_WORKERS):
        ddk = self.columns['session_service_workers.csv']
        UPDATED_SERVICE_WORKERS = {k: [] for k in ddk}
        for i in range(len(SERVICE_WORKERS)):
            for j in range(len(ddk)):
                service_worker_row = SERVICE_WORKERS[i].to_row()
                UPDATED_SERVICE_WORKERS[ddk[j]].append(service_worker_row[j])
        self.save_dict('session_service_workers.csv', UPDATED_SERVICE_WORKERS)

    def update_sessions(self, SESSIONS):
        ddk = self.columns['session_sessions.csv']
        UPDATED_SESSIONS = {k: [] for k in ddk}
        for i in range(len(SESSIONS)):
            for j in range(len(ddk)):
                session_row = SESSIONS[i].to_row()
                UPDATED_SESSIONS[ddk[j]].append(session_row[j])
        self.save_dict('session_sessions.csv', UPDATED_SESSIONS)
        
    def update_service_worker(self, service_worker):
        SERVICE_WORKERS = self.load_service_workers()
        for i, curr_service_worker in enumerate(SERVICE_WORKERS):
            if curr_service_worker.name == service_worker.name:
                curr_service_worker.users = service_worker.users
                curr_service_worker.operations = service_worker.operations
                break
        self.update_service_workers(SERVICE_WORKERS)






def __view_sessions():
    uss = USS('session')
    USERS = uss.load_users()
    SESSIONS = uss.load_sessions()
    SERVICE_WORKERS = uss.load_service_workers()
    
    if DEVELOPMENT == 'TRUE': print("__view_sessions() breakpoint for viewing here")

def endpoint_add_service_worker(name):
    uss = USS('session')
    USERS = uss.load_users()
    SESSIONS = uss.load_sessions()
    SERVICE_WORKERS = uss.load_service_workers()
    if name not in [s.name for s in SERVICE_WORKERS]:
        SERVICE_WORKERS.append(ServiceWorker(name, [], []))
        uss.update_service_workers(SERVICE_WORKERS)
        __view_sessions()
        return f"Service worker {name} added."
    
    __view_sessions()
    return f"Service worker {name} already in service worker pool."


def endpoint_remove_service_worker(name):
    uss = USS('session')
    USERS = uss.load_users()
    SESSIONS = uss.load_sessions()
    SERVICE_WORKERS = uss.load_service_workers()
    if name in [s.name for s in SERVICE_WORKERS]:
        SERVICE_WORKERS = [s for s in SERVICE_WORKERS if s.name != name]
        uss.update_service_workers(SERVICE_WORKERS)
        __view_sessions()
        return f"Service worker {name} removed from service worker pool."
    return f"Service worker {name} hasn't been added to service worker pool yet."


def endpoint_authorize_user_for_service_worker(username, service_worker_name):

    def already_authorized(un, swn):
        uss = USS('session')
        SESSIONS = uss.load_sessions()
        for s in SESSIONS:
            if s.user_id == un and s.woker_id and swn:
                return True        
        return False
    
    uss = USS('session')
    if not already_authorized(username, service_worker_name):
        user = uss.get_user(username)
        service_worker = uss.get_service_worker(service_worker_name)
        service_worker.users.append(user)
        uss.update_service_worker(service_worker)
        __view_sessions()
        return f"User {username} authorized for {service_worker_name}."
    return f"User {username} already authorized for {service_worker_name}."


def endpoint_create_session(username):
    uss = USS('session')
    USERS = uss.load_users()
    SESSIONS = uss.load_sessions()
    SERVICE_WORKERS = uss.load_service_workers()
    if username in [u.username for u in USERS]:
       return f"User {username} already in users."
    if not SERVICE_WORKERS:
       return f"No service workers available."


    user = get_user_by_username(username)
    user_access_level = user.user_info["ACCOUNT_TYPE"]
    user = User(username, user_access_level)
    USERS.append(user)  # plc args
    uss.update_users(USERS)
    for service_worker in SERVICE_WORKERS:
        if username in [u.name for u in service_worker.users]:
            __view_sessions()
            return f"User {username} already authorized for {service_worker.name}"
        else:
            session = Session(username, service_worker.name)  # missing max time
            SESSIONS.append(session)
            uss.update_sessions(SESSIONS)
            endpoint_authorize_user_for_service_worker(username, service_worker.name)
            __view_sessions()
            return f"User {username} added to {service_worker.name}"
        

def endpoint_delete_session(user_id, worker_id):
    uss = USS('session')
    USERS = uss.load_users()
    USERS = [u for u in USERS if u.username != user_id]
    uss.update_users(USERS)

    
    SERVICE_WORKERS = uss.load_service_workers()
    for sw in SERVICE_WORKERS:
        if sw.name == worker_id:
            sw.users = [u for u in sw.users if u.username != user_id]
            break
    uss.update_service_workers(SERVICE_WORKERS)
    
    SESSIONS = uss.load_sessions()
    SESSIONS = [s for s in SESSIONS if not (s.user_id == user_id and s.worker_id == worker_id)]
    uss.update_sessions(SESSIONS)

    __view_sessions()
    return f"Deleted session!"


def endpoint_add_operation(worker_id: str, operation: dict):
    uss = USS('session')
    SERVICE_WORKERS = uss.load_service_workers()
    for sw in SERVICE_WORKERS:
        if sw.name == worker_id:
            sw.operations.append(operation)
            uss.update_service_workers(SERVICE_WORKERS)
            __view_sessions()
            return f"Added operation to {sw.name}'s task queue."
    __view_sessions()
    return f"Service worker: {worker_id}'s has not been connected."


def get_operations_by_worker_id(worker_id):
    uss = USS('session')
    SERVICE_WORKERS = uss.load_service_workers()
    for sw in SERVICE_WORKERS:
        if sw.name == worker_id:
            return sw.operations
    __view_sessions()
    return []


def get_available_service_workers() -> list[str]:
    uss = USS('session')
    SERVICE_WORKERS = uss.load_service_workers()
    available = []
    for sw in SERVICE_WORKERS:
        temp = sw.operations
        if not sw.users and not sw.operations:
            available.append(sw.name)
    return available


