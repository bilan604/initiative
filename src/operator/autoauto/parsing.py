import re
import openai
import base64
import string
import requests
from bs4 import BeautifulSoup


# function name is depreciated
def get_openai_result(prompt):
    if type(prompt) != str:
        return
    if len(prompt) == 0:
        return "Empty Query Recieved"

    response = openai.Completion.create(model="text-davinci-003",
                                        prompt=prompt,
                                        max_tokens=1800)
    return response.choices[0].text.strip()


def get_env(file_path=".env"):
    env = {}
    with open(file_path, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line:
                lst = line.split("=")
                env[lst[0].strip()] = lst[1].strip()
    return env

def encrypt_string(string):
    encoded_bytes = base64.b64encode(string.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string

def decrypt_string(encoded_string):
    decoded_bytes = base64.b64decode(encoded_string.encode('utf-8'))
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string

def get_text(s):
    s = re.sub("<.+?>", "\n", s)
    s = re.sub("{.+?}", "\n", s)
    s = re.sub("\(.+?\)", "\n", s).strip()
    return s

def parse_spacing(s):
    s = parse_newline_spacing(s)
    s = re.sub("\n", " ", s)
    s = re.sub(" +", " ", s)
    s = s.strip()
    return s

def get_text(s):
    s = re.sub("<.+?>", "\n", s)
    s = re.sub("{.+?}", "\n", s)
    s = re.sub("\(.+?\)", "\n", s)
    s = s.strip()
    return s

def parse_newline_spacing(s):
    s = re.sub("( |\n)+\n( |\n)+", "\n", s)
    s = re.sub("\n+", "\n", s)
    s = s.strip()
    return s

def parse_spacing(s):
    s = parse_newline_spacing(s)
    s = re.sub("\n", " ", s)
    s = re.sub(" +", " ", s)
    return s

def parse_src_text(s):
    ots = list('{[<')
    cts = list('}]>')

    depth = []
    ans = []
    add = False
    curr = ""
    for letter in s:
        if letter in ots:
            if not depth:
                ans.append(curr)
                curr = ""
                depth.append(letter)
                add = False
            else:
                ans.append(curr)
            
        elif letter in cts:
            if depth and ots.index(depth[-1]) == cts.index(letter):
                depth.pop()
            if not depth: # and not add
                add = True
        else:
            if add:
                curr += letter
    ans = [si.strip() for si in ans if len(si.strip()) > 1]
    ans = [si for si in ans if len(re.sub("[^a-zA-Z]", "", si)) * 2 >= len(si)]
    return "\n".join(ans)            


def format_rows(s, n=100):
    """
Makes things print pretty
    """

    rows = []
    for row in s.split("\n"):
        if len(row) <= 100:
            rows.append(row)
        else:
            curr = []
            for word in row.split(" "):
               
                if len(" ".join(curr)) + len(word) + 1 > 100:
                    rows.append(" ".join(curr))
                    curr = []
               
                curr.append(word)
           
            if curr:
                rows.append(" ".join(curr))
    return "\n".join(rows)

def indent(s):
    # adds tabs to s
    s = format_rows(s).strip()
    return "\n".join(["    "+row.strip() for row in s.split("\n")])

temp = """
                            B)"__SEARCH__"
                            Extracting the content from the search result urls.

                            E)"__STORE__"
                            Description: Within subtasks, your previous response is provided to you inside all prompts for reference/convenience by default. You can replace the content that will be stored with this command.
                            INPUT: your response

                            F)"__EXEC__"
                            Description: Execute a chunk of Python code.\
                            INPUT: your response
"""

def format(label:str, content: str):
    if content == "":
        return ""
    s = \
    f"""\
{label}:
\"\"\"\"\"\"
{content}
\"\"\"\"\"\"

"""
    return s

def filter_spacing(s):
    s = re.sub("\n+?", " ", s)
    s = re.sub(" +", " ", s)
    return s.strip()

#################### defined in api.py
def get_openai_result(prompt):
  if type(prompt) != str:
    return
  if len(prompt) == 0:
    return "Empty Query Recieved"

  response = openai.Completion.create(model="text-davinci-003",
                                      prompt=prompt,
                                      max_tokens=2000)
  return response.choices[0].text.strip()


def get_verdict(resp, product, text, link):
  text = text[:min(2000, len(text))]
  #############
  target = resp ############
  prompt = f"The following text is from the {product.tag} HTML tag element of {link}.\n\nText:\n"
  prompt += f"\"\"\"\n{text.strip()}\"\"\"\n\n"
  prompt += "Please determine whether the tag represents a " + target  + " on the website. "
  #Adds Example
  #prompt += "(i.e. Is selling/marketing a service, lists benefits, different payment plans, etc). "
  prompt += "If the content represents " + target + " respond with \"YES:" + target + "\". If the content represents multiple "+target+", respond with \"YES:"+target+"_LISTING\". Otherwise, respond with \"NO:\" followed by a classification (i.e. \"NO:ANNOUNCEMENT\", \"NO:SEARCH_BAR\", \"NO:DISCLAIMER\").\n\n"
  resp = get_openai_result(prompt)
  print(f"{prompt=}\n")
  print(f"{resp=}\n")
  print("----------------------------------")
  return resp

def get_response_(url):

  timeout = 10  # Timeout duration in seconds
  response = None
  try:
    response = requests.get(url, timeout=timeout)
    # Process the response here
    if "200" not in str(response):
      return None
  except requests.Timeout:
    # Handle timeout exception
    print("Request timed out.")
  except requests.RequestException as e:
    # Handle other request exceptions
    print("Request error:", str(e))
  return response

def deduplicate_newlines(tasks: str):
    tasks = re.sub("\n+?", "\n", tasks)
    return tasks


def contains_url(string):
    pattern = r"[http[s]?://]?[www\.]?[a-zA-Z|0-9]{3,30}[\.][a-z]{3,20}[(/a-z)]?"
    match = re.search(pattern, string)
    return bool(match)

def count_urls(s):
    s = re.sub("(https)(://)?www\.([a-zA-Z0-9]{2,30})(\.)([a-z]{1,15})(/[a-z]+)?(/)?", "__LINK__", s)
    return s.count("__LINK__")

def get_url(s):
    s = s.strip()
    return s


def get_mask_count(resp):
    mask = re.sub("__[A-Z]{3,25}__", "__||||__", resp)
    return mask.count("__||||__")

def is_bad(task):
    print("CHECKING SUBTASK")
    print("task:", task, "<=||")
    if not task:
        return True
    if "\"\"\"" in task.lower():
        return True
    if "'''" in task.lower():
        return True
    if "__subtasks__" in task.lower():
        return True
    if "__searchquery__" in task.lower():
        return True
    if "__visit__" in task.lower():
        return True
    if "objective:" in task.lower():
        return True
    if "original:" in task.lower():
        return True
    if "response:" in task.lower():
        return True
    if ":" in task.lower():
        if contains_url(task):
            urlCount = count_urls(task)
            if urlCount != task.count(":") or urlCount != 1:
                return False
    return False


def parseQuery(resp):
    letters = string.ascii_lowercase
    splitter = "__SEARCHQUERY__:"
    idx = resp.find(splitter)
    resp = resp[idx+len(splitter):]
    resp = resp.strip()

    while resp and resp[0].lower() not in letters:
        resp = resp[1:]
    while resp and resp[-1].lower() not in letters:
        resp = resp[:-1]

    return resp

    
def parse_subtasks(subtasks):
    subtasks = deduplicate_newlines(subtasks.strip())         
    splitter = "__SUBTASKS__:"
    idx = subtasks.find(splitter)
    if idx == -1:
        return ""
    if idx == subtasks.find(splitter+"\n"):
        splitter += "\n"
    subtasks = subtasks[subtasks.find(splitter)+len(splitter):]
    subtasks = re.sub("\<.+?\>", "", subtasks)
    subtasks = re.sub("\(.+?\)", "", subtasks)
    subtasks = subtasks.strip()
    subtasks = [s.strip() for s in subtasks.split("\n") if s.strip()]
    return subtasks






