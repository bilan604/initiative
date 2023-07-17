import re
from bs4 import BeautifulSoup


def contains_url(string):
    pattern = r"[http[s]?://]?[www\.]?[a-zA-Z|0-9]{3,30}[\.][a-z]{3,20}[(/a-z)]?"
    match = re.search(pattern, string)
    return bool(match)


def parse_text_spacing(s):
    """
    This function removes the HTML tags and extracts uniformly spaced text
    """
    words = re.sub("<.+?>", "", s)
    words = re.sub("\n+", "\n", words)
    words = re.sub(" +", " ", words)
    words = " ".join([w.strip() for w in words.split(" ") if w.strip()])
    words = words.strip()
    return words

def getWords(s):
    words = re.sub("<\\//.+?>", "<[/element]>", s)
    words = re.sub("<.+?>", "<[element]>", words)
    words = re.sub("\n+", "\n", words)
    words = re.sub(" +", " ", words)
    words = " ".join([w.strip() for w in words.split(" ") if w.strip()])
    words = words.strip()
    return words


def get_text(s):
    s = re.sub("<.+?>", "\n", s)
    s = re.sub("\[.+?\]+", "\n", s)
    s = re.sub("{.+?}", "\n", s)
    return s


def get_uniform_spacing(s):
    s = re.sub(" +", " ", s)
    return s

def getTags(s):
    # in getNestedTags
    ans = []
    curr = ""
    depth = 0
    for letter in s:
        if letter == "<":
            add = True
        elif letter == ">":
            add = False
            if curr:
                ans += ["<"+curr+">"]
                curr = ""
        else:
            if add:
                curr += letter
    return ans


def getMaxDepth(s):
    # in getNestedTags
    tags = getTags(s)
    m = 0
    curr = 0
    for tag in tags:
        if tag[:2] == "</" or tag[-2:] == "/>":
            curr -= 1
        else:
            curr += 1
            m = max(m, curr)
    return m
def getNestedTags(s):
    # gets tags with 1 less max depth, so the immediate children only
    elements = BeautifulSoup(s, 'html.parser').find_all()
    elements = list(map(str, elements))
    ans = []

    dd = {}
    for element in elements:
        maxDepth = getMaxDepth(element)
        if maxDepth not in dd:
            dd[maxDepth] = []
        dd[maxDepth] += [element]
    rkey = sorted(list(dd.keys()))
    if len(rkey) >= 2:
        return dd[rkey[-2]]
    return dd[rkey[-1]]

def parseLetterSpacing(s):
    # returns evenly spaced letters
    s = re.sub("[^a-zA-Z| ]", "", s.strip())
    s = re.sub(" +", " ", s)
    return s


##############################
def contains_url(string):
    pattern = r"[http[s]?://]?[www\.]?[a-zA-Z|0-9]{3,30}[\.][a-z]{3,20}[(/a-z)]?"
    match = re.search(pattern, string)
    return bool(match)


def getTags(htmlContent):
    if htmlContent.find("<body") != 0:
        soup = BeautifulSoup(htmlContent, "html.parser")
        htmlContent = str(soup.find_all("body")[0])
        
    soup = BeautifulSoup(htmlContent, "html.parser")
    tags = soup.find_all()
    tags = list(map(str, tags))
    return tags


def getWords(s):
    words = re.sub("<\\//.+?>", "<[/element]>", s)
    words = re.sub("<.+?>", "<[element]>", words)
    words = re.sub("\n+", "\n", words)
    words = re.sub(" +", " ", words)
    words = " ".join([w.strip() for w in words.split(" ") if w.strip()])
    words = words.strip()
    return words


def parseAnswerTextSpacing(s):
    # Lowercase version
    s = s.lower().strip()
    s = re.sub("[a-zA-Z| ]", "", s)
    s = re.sub(" +", " ", s)
    s = s.strip()
    return s


def remove_escape_sequences(qa):
    newQa = ""
    for i in range(len(qa)):
        letter = qa[i]
        if letter == "\\":
            if i == 0:
                pass
            elif i == len(qa) - 1:
                pass
            else:
                if not (qa[i-1] == "<" or qa[i+1] == ">"):
                    pass
                else:
                    newQa += letter
        else:
            newQa += letter
    return newQa.strip()


def parseLstOfJsonStrs(s):
    jsons = []
    stack = 0
    curr = ""
    add = False
    for letter in s:
        if letter == "{":
            add = True
            # Ensures only depth 1 curly braces are parsed
            if stack == 0:
                stack += 1
        elif letter == "}":
            stack -= 1
            if stack == 0:
                jsons.append("{"+curr+"}")
                add = False
                curr = ""
        else:
            if add:
                curr += letter
            else:
                pass
    return jsons


def handle_parse_json(qa, expected_keys=3):
    # parses a json object
    if len(qa) < 2:
        return None
    dd = {}
    qa = qa[1:-1]
    qa = qa.split(",")
    qa = [qa.split(":") for qa in qa]
    qa = [q_a for q_a in qa if len(q_a) == 2]
    if len(qa) != expected_keys:
        return None
    qa = [[q_a[0].strip(), q_a[1].strip()] for q_a in qa]
    for q_a in qa:
        if not q_a[0] or not q_a[1]:
            return None
        k = re.sub("\"", "", q_a[0])
        k = remove_escape_sequences(k)
        v = re.sub("\"", "", q_a[1])
        v = remove_escape_sequences(v)
        dd[k] = v
    return dd


def load_response(response):
    response = "".join(response.split("TRUE:")[1:])
    response_object = parseLstOfJsonStrs(response)
    loaded_responses = []
    for question_answer in response_object:
        question_answer = handle_parse_json(question_answer)
        if not question_answer:
            continue
        loaded_responses.append(question_answer)
    return loaded_responses







