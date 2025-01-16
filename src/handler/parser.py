import re
from bs4 import BeautifulSoup
from src.generic.loader import get_env_variable


DEVELOPMENT = get_env_variable('DEVELOPMENT')

def getText(e: str):
    # This removes everything inside an opening and closing tag
    # from html code, given that the tags are properly nested
    stack = []
    texts = []
    curr = ""
    for i in range(len(e)):
        if e[i] == "<":
            if not stack:
                texts.append(curr)
                curr = ""
            stack.append("<")  # arbituray letter
        elif e[i] == ">":
            if not stack:
                if DEVELOPMENT == 'TRUE': print("the HTML code has uneven opening and closing elements")
                return ""
            stack.pop()
        else:
            if not stack:
                curr += e[i]
    if curr:
        texts.append(curr)

    return "".join(texts)

def simplify(s: str):
    # converts HTML code to uniformly spaced lowercase letters (words)
    # note: some text may be white on the webpage
    if type(s) != str:
        return ""
    s = s.lower()
    s = re.sub("[^a-zA-Z|0-9|\-|\%| ]", " ", s)
    s = re.sub(" +", " ", s)
    s = s.strip()
    return s

def simplifyHTML(s):
    # converts HTML code to uniformly spaced lowercase letters (words)
    # note: some text may be white on the webpage
    s = getText(s).strip()
    s = re.sub("\n", " ", s)
    s = re.sub(" +", " ", s)
    s = re.sub("[^a-zA-Z| ]", "", s)
    s = s.lower()
    s = s.strip()
    return s

def getTag(element):
    idx = element.find(">")
    if not idx:
        return ""
    return element[:idx+1]

def getOpeningTag(element):
    if not element:
        return ""
    idx = element.find(">")
    if idx == -1:
        return ""
    return element[:idx+1]

def getProperties(tag: str):
    # 09/01/2023: version
    # fix href url values &amp; => & and = sign causing multiple hrefs (= signs nested inside the value)
    if not tag:
        if DEVELOPMENT == 'TRUE': print("get_properties(): empty tag")
        return {}
    
    if getOpeningTag(tag) != tag:
        tag = getOpeningTag(tag)
    
    
    def __get_property_name(tag, idx):
        for i in range(idx, -1, -1):
            if tag[i] == " ":
                return tag[i:idx].strip()
        return ""
    
    def __get_property_value(tag, idx):
        tag = tag[idx:]
        quotation_marks = 0
        property_value = ""
        for i, letter in enumerate(tag):
            if letter == '"':
                quotation_marks += 1
            else:
                if quotation_marks == 1:
                    property_value += letter
                elif quotation_marks == 2:
                    return property_value
                else:
                    pass
        return property_value
        
    if len(tag) <= 3:
        return {}
    
    idx = tag.find(" ")
    if idx == -1:
        return {}

    property_values = {}

    tag = tag[idx:-1]
    for i in range(len(tag)):
        if tag[i] == "=":
            property_name = __get_property_name(tag, i)
            property_value = __get_property_value(tag, i)
            if "=" in property_name:
                continue
            property_value = re.sub('&amp;', '&', property_value)
            property_values[property_name] = property_value
    return property_values

def getText(element: str):
    element = re.sub("<.+?>", "", element).strip()
    return element

def getQuestion(text, divs):
    for div in divs:
        if text in div:
            return div
    return None

def get_xpath_by_element(element):
    # returns a chrome selenium xpath
    if not element:
        if DEVELOPMENT == 'TRUE': print("get_xpath_by_element(): empty element")
        return None
    element_type = element[1: element.find(" ")]
    opening_tag = getOpeningTag(element)
    properties = getProperties(opening_tag)
    if "id" in properties:
        properties = {"id": properties["id"]}
    
    xpath_identifiers = [f"@{property_name}='{property_value}'" for property_name, property_value in properties.items()]
    xpath_identifier = " and ".join(xpath_identifiers)
    xpath = f"//{element_type}[{xpath_identifier}]"
    return xpath

def get_xpath_by_properties(element_type, properties):
    xpath_identifiers = [f"@{property_name}='{property_value}'" for property_name, property_value in properties.items()]
    xpath_identifier = " and ".join(xpath_identifiers)
    xpath = f"//{element_type}[{xpath_identifier}]"
    return xpath

def getElements(src, elementType):
    soup = BeautifulSoup(src, 'html.parser')
    elements = soup.find_all(elementType)
    elements = list(map(str, elements))
    return elements

from bs4 import BeautifulSoup

##############
# the following are from webhelper
def getElements(src, elementType: str):
    soup = BeautifulSoup(src, 'html.parser')
    elements = soup.find_all(elementType)
    elements = list(map(str, elements))
    return elements

def getElementTextsDict(__text, elementType):  
    # arg __text is unused and isn't required here
    # !!!! RETURNS str: list[dict]!!!!!!!!
    
    els = getElements(elementType)
    dd = {}
    for el in els:
        text = getText(el)
        if text not in dd:
            dd[text] = []
        dd[text] += [el]
    return dd

def getElementsBySimplifiedText(elementType) -> dict[str, str]:
    els = getElements(elementType)
    dd = {}
    for el in els:
        text = simplifyHTML(el)
        if text not in dd:
            dd[text] = el
        else:
            if len(el) < len(dd[text]):
                dd[text] = el
    return dd

def editDistance(word1: str, word2: str) -> int:
    word1 = "-" + word1
    word2 = "-" + word2
    m = len(word1)
    n = len(word2)

    # Initialize the dp table
    dp = [[0] * (n) for _ in range(m)]

    # Base cases
    for i in range(m):
        dp[i][0] = i
    for j in range(n):
        dp[0][j] = j

    # Fill in the dp table
    for i in range(1, m):
        for j in range(1, n):
            if word1[i] == word2[j]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j-1], dp[i][j-1], dp[i-1][j])
    return dp[m-1][n-1]

def matchStrings(targ: str, strings: list):
    ans = ""
    score = 9999999
    for si in strings:
        sci = editDistance(targ.lower().strip(), si.lower().strip())
        if sci <= score:
            ans, score = si, sci
    return ans

def getElementByText(text, elementType):
    # uses levensctein
    elsDict = getElementTextsDict(text, elementType)
    key = matchStrings(text, list(elsDict.keys()))
    #if len more than one
    return elsDict[key][0]


def getElementByLabel(text: str, elementType: str):
    # uses direct match of s.lower().strip()
    elementLabelsDict = getElementTextsDict(text, elementType)
    key_simplifier = {label.lower().strip(): label for label in elementLabelsDict}
    if text.lower().strip() in key_simplifier:
        return elementLabelsDict[key_simplifier[text.lower().strip()]][0]
    return None

def getElementByLabelContains(text, elementType):
    # newer than above
    text = simplifyHTML(text)  # sample effect as simplify
    elementLabelsDict = getElementsBySimplifiedText(elementType)
    for key in elementLabelsDict:
        if text in key:  # if label contains
            return elementLabelsDict[key]
    return None

def getXpathByText(text, elementType):
    # uses levensctein
    el = getElementByText(text, elementType)
    xpath = get_xpath_by_element(el)
    return xpath

def getXpathByLabel(text, elementType):
    el = getElementByLabel(text, elementType)
    xpath = get_xpath_by_element(el)
    return xpath

def getXpathByLabelContains(text, elementType):
    el = getElementByLabelContains(text, elementType)
    xpath = get_xpath_by_element(el)
    return xpath

def getButtonByLabelContains(text):
    return getXpathByLabelContains(text, 'button')


def getTags(s):

    def getTags1(s):
        tags = []
        curr = ""
        indiv = False
        for i in range(len(s)):
            if s[i] == "<":
                tags.append(curr)
                curr = s[i]
                indiv = True
            elif s[i] == ">":
                curr+=s[i]
                tags.append(curr)
                curr = ""
                indiv = False
            else:
                curr += s[i]

        if curr:
            tags.append(curr)

        tags = [re.sub("\n", "", tag.strip()) for tag in tags]
        tags = [tag for tag in tags if tag]
        return tags

    def getTags2(s):
        tags = []
        curr = ""
        indiv = [] # a stack used to check boolean condition of s[i] is inside a div
        for i in range(len(s)):
            if s[i] == "<":
                tags.append(curr)
                curr = s[i]
                indiv.append("<")
            elif s[i] == ">":
                if not indiv:
                    if DEVELOPMENT == 'TRUE': print("Balance error")
                    continue
                indiv.pop()
                if not indiv:
                    curr+=s[i]
                    tags.append(curr)
                    curr = ""
            else:
                curr += s[i]

        if curr:
            tags.append(curr)

        tags = [re.sub("\n", "", tag.strip()) for tag in tags]
        tags = [tag for tag in tags if tag]
        return tags
    
    
    tags1 = getTags1(s)
    # note: slow
    # time will tell if this is an issue
    tags2 = getTags2(s)  # getTags2 checks for nested <
    if tags1 != tags2:
        if DEVELOPMENT == 'TRUE': print("NOTE: tags1 != tags2, there was a < nesting discrepancy in the element")
        return tags2
    return tags2



