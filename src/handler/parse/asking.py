###########################################################
# Now: Application helper parsing funcs
###########################################################
import re
import string
from bs4 import BeautifulSoup


def get_text(s, remove_javascript=True):
    """
    Returns English
    """
    s = re.sub("<.+?>", "\n", s)
    if remove_javascript:
        s = re.sub("\[.+?\]+", "\n", s)
        s = re.sub("{.+?}", "\n", s)
    s = s.strip()
    return s

def parse_text_spacing(s):
    """
    The function name
    """
    s = re.sub("\n", " ", s)
    s = re.sub(" +", " ", s)
    s = s.strip()
    return s

def get_spaced_words(s):
    s = get_text(s)
    s = re.sub("[^a-zA-Z]", " ", s)
    s = parse_text_spacing(s)
    return s

def get_tags(s):
    # in getNestedTags
    ans = []
    curr = ""
    add = False
    for letter in s:
        if letter == "<":
            if depth == 0:
                add = True
            depth += 1
        elif letter == ">":
            if depth == 0:
                print("get_tags() Error: Unbalanced angle brackets in string")
                curr = ""
                # buffer
                depth = 1
            depth -= 1
            if depth == 0:
                add = False
            if curr:
                ans += ["<"+curr+">"]
                curr = ""
        else:
            if add:
                curr += letter
    return ans


def get_opening_tag(element):
    if not element:
        print("get_opening_tag(): empty element")
        return None
    return element[:element.find(">")+1]

def get_xpath_by_properties(element_type, properties):
    xpath_identifiers = [f"@{property_name}='{property_value}'" for property_name, property_value in properties.items()]
    xpath_identifier = " and ".join(xpath_identifiers)
    xpath = f"//{element_type}[{xpath_identifier}]"
    return xpath

def get_xpath_by_element(element, element_type="button"):
    if not element:
        print("get_xpath_by_element(): empty element")
        return None
    opening_tag = get_opening_tag(element)
    properties = get_properties(opening_tag)
    if "id" in properties:
        properties = {"id": properties["id"]}
    
    xpath_identifiers = [f"@{property_name}='{property_value}'" for property_name, property_value in properties.items()]
    xpath_identifier = " and ".join(xpath_identifiers)
    xpath = f"//{element_type}[{xpath_identifier}]"
    return xpath


def get_input_xpath(element, property_name=""):
    if not element:
        print("get_xpath_by_element(): empty element")
        return None
    opening_tag = get_opening_tag(element)
    properties = get_properties(opening_tag)
    if "id" in properties:
        properties = {"id": properties["id"]}
    
    xpath_identifiers = [f"@{property_name}='{property_value}'" for property_name, property_value in properties.items()]
    xpath_identifier = " and ".join(xpath_identifiers)
    xpath = f"//input[{xpath_identifier}]"
    return xpath



def get_targeted_texts(src, element_type="", parameters={}):
    """
    Wrapper function for soup.find_all and getting text
    """
    soup = BeautifulSoup(src, 'html.parser')
    tags = soup.find_all(element_type, parameters)
    tags = list(map(str, tags))
    tags = [get_text(tag) for tag in tags]
    return tags



def get_elements(src, element_type, properties_rule, text_rule):
    elements = BeautifulSoup(src, 'html.parser').find_all(element_type)
    elements = list(map(str, elements))
    elements = sorted(elements, key=lambda x:len(x))
    answer = []
    vis = set({})
    for element in elements:
        properties = get_properties(element)

        if properties_rule(properties):
            text = get_text(element).strip()
            if text_rule(text) and text not in vis:
                vis.add(text)
                answer.append(element)
    return answer


def get_property_value_from_tag(tag, property_name):
    """
    gets the value of a property in an opening tag
    """
    for i in range(len(tag)-len(property_name)):
        if tag[i:i+len(property_name)] == property_name:
            s = tag[i+len(property_name)+1:]
            s = s[:s.index('"')]
            return s
    return ""


# BAD
def get_elements_by_value_rule(src="", element_type="div", property_name="id", rule=lambda x: "summary" in x):
    """
    finds an element with some proprty value matching a specified rule
    """
    elements = BeautifulSoup(src, 'html.parser').find_all(element_type)
    elements = list(map(str, elements))
    elements = sorted(elements, key=lambda x:len(x))
    ans  = []
    for element in elements:
        opening_tag = get_opening_tag(element)        
        properties = get_properties(opening_tag)
        if property_name in properties and rule(properties[property_name]):
            ans.append(element)
    return ans

def get_element_by_text_rule(src, element_type, rule):
    """
    src: The html of the page
    element_type: the type of element being searched for
    rule: a rule for matching the text contained in the button, i.e. a button label
    """
    elements = BeautifulSoup(src, 'html.parser').find_all(element_type)
    elements = list(map(str, elements))
    elements = sorted(elements, key=lambda x:len(get_text(x).strip()))
    for element in elements:
        text = get_text(element).strip()
        if rule(text):
            return element
    return ""


def get_element_values(src, element_type="a", property_name = "href"):
    elements = BeautifulSoup(src).find_all(element_type)
    elements = list(map(str, elements))
    ans = []
    for element in elements:
        properties = get_properties(element)
        if property_name in properties:
            ans.append(properties[property_name])
    return ans

################################################
##################################################
#################################################
import re
import string
from bs4 import BeautifulSoup


def get_text(s):
    s = re.sub("<.+?>", "\n", s)
    s = re.sub("\[.+?\]+", "\n", s)
    s = re.sub("{.+?}", "\n", s)
    return s

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

def get_tags(s):
    # in getNestedTags
    ans = []
    curr = ""
    add = False
    for letter in s:
        if letter == "<":
            add = True
        elif letter == ">":
            add = False
            if curr:
                ans.append("<" + curr + ">")
                curr = ""
        else:
            if add:
                curr += letter
    return ans


def get_properties(tag):
    """
    Returns a dictionary containing the property_names and property values of an opening tag as the key:value pairs
    """
    if not tag:
        print("get_properties(): empty tag")
        return {}
    
    if get_opening_tag(tag) != tag:

        tag = get_opening_tag(tag)
    
    
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
            property_values[property_name] = property_value
    return property_values


def get_targeted_element(src, element_type, targeted_text):
    """
    Gets an html element containing the targeted label text
    """
    anchors = BeautifulSoup(src, 'html.parser').find_all(element_type)
    anchors = list(map(str, anchors))
    anchors = sorted(anchors, key=lambda x: len(x))
    anchor_texts = [get_text(anchor).lower().strip() for anchor in anchors]
    for i, at in enumerate(anchor_texts):
        if at == targeted_text:
            return anchors[i]
    return ""


def get_element_by_text_rule(src, element_type, rule):
    elements = BeautifulSoup(src, 'html.parser').find_all(element_type)
    elements = list(map(str, elements))
    elements = sorted(elements, key=lambda x: len(get_spaced_words(x)))

    for element in elements:
        text = parse_text_spacing(get_text(element)).strip()
        if rule(text):
            print("returing button with label", text)
            return element
    return ""



def get_xpath_by_properties(element_type, properties):
    """
    Takes a dictionary of property name, property values from the opening tag
    of an html element and returns a xpath.
    """
    xpath_identifiers = []

    if "id" in properties:
        element_id = properties["id"]
        return f"//{element_type}[@id='{element_id}']"

    for property_name, property_value in properties.items():
        xpath_identifiers.append(f"@{property_name}='{property_value}'")
    
    xpath_identifier = " and ".join(xpath_identifiers)
    xpath = f"//@{element_type}[{xpath_identifier}]"
    return xpath


def get_element(src, element_type, label_rule, properties_rule):
    elements = BeautifulSoup(src, 'html.parser').find_all(element_type)
    elements = list(map(str, elements))
    elements = [[element, parse_text_spacing(get_text(element)).strip()] for element in elements]
    elements = sorted(elements, key=lambda x: len(x[1]))
    for element, element_label in elements:
        if label_rule:
            if label_rule(element_label):
                if not properties_rule:
                    return element
                properties = get_properties(element)
                if properties_rule(properties):
                    return element
    return ""
            
    
def get_elements_by_src(src, element_type="", parameters={}):
    """
    BeautifulSoup for some reason returns matches where the parameter keys are present in the element, but
    the value only contains the argument
    <div class='abc def' .... is returned by find_all('div', {'class': 'def'})
    
    So this function makes it require an exact match for values, which is what I always thought it was...
    """
    if parameters and not element_type:
        print("get_elements_by_src() Input error? Check <-----------")
        return {}
        
    if not element_type and not parameters:
        elements = BeautifulSoup(src, 'html.parser').find_all()
    if element_type and not parameters:
        elements = BeautifulSoup(src, 'html.parser').find_all(element_type)
    if element_type and parameters:
        elements = BeautifulSoup(src, 'html.parser').find_all(element_type, parameters)

    def is_exact_match(element, parameters):
        opening_tag = get_opening_tag(element)
        element_properties = get_properties(opening_tag)
        for required_property_name in parameters:
            if required_property_name not in element_properties:
                return False
            if element_properties[required_property_name] != parameters[required_property_name]:
                return False
        return True


    elements = list(map(str, elements))
    if parameters:
        # a filter
        # elements with exact matches to the values in the parameter dict
        double_validation = []
        for element in elements:
            if is_exact_match(element, parameters):
                double_validation.append(element)
        return double_validation
    return elements
    
########################
