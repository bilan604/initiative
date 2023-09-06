import os
import openai

def get_env(file_path=".env"):
    env = {}
    with open(file_path, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line:
                lst = line.split("=")
                env[lst[0].strip()] = lst[1].strip()
    return env

def load_env(environment="development"):
    # ToDo: implement
    env = get_env()
    OPENAI_API_KEY = env["OPENAI_API_KEY"]
    openai.api_key = OPENAI_API_KEY
    return

def get_handler_env():
    env = get_env('.env')
    return env['DEVELOPMENT']

def update_src_env(DEVELOPMENT):
    rep = 'False'
    if DEVELOPMENT == True:
        rep = 'True'
    src_env = get_env('.env')
    src_env['DEVELOPMENT'] = rep
    with open('.env', 'w+') as f:
        for k, v in src_env.items():
            f.write('='.join([k,v])+"\n")
    
    return

def get_files(directory):
    cwd = os.getcwd()

    os.chdir(cwd + "/" + directory)

    files = []
    for file in os.listdir():
        if os.path.isfile(file):
            files.append(file)

    os.chdir(cwd)
    return files