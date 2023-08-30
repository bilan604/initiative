import re
import json
import requests
from bs4 import BeautifulSoup

from src.operator.autoauto.parsing import *
from src.operator.autoauto.api import prompt_gpt_3_5_turbo


def get_links_from_tag(anchor_tags):
  ans = []
  anchor_tags = [str(tag) for tag in anchor_tags]
  for tag in anchor_tags:
    if 'href="/url?q=' not in tag:
      continue
    elements = tag.split('href="/url?q=')
    
    item = elements[1]
    item = item[:item.index("\"")]
    ans.append(item)
  return ans


def get_divs(s):
    inTag = False
    currString = ""
    response = []
    for letter in s:
        if letter == "<":
            inTag = True
            if currString:
                response.append(currString)
            currString = ""
        elif letter == ">":
            inTag = False
        else:
            if not inTag:
                currString += letter
    if currString:
        response += currString
    
    return response

def filter_by_contains_property(property_names, tags):
    filtered_tags = []
    for tag in tags:
        if type(tag) != str:
            tag = str(tag)
        matching_properties = 0
        property_values = tag.split(" ")
        for property_value in property_values:
            if "=" not in property_value:
                continue
            if property_value.split("=")[0] in property_names:
                matching_properties += 1
        if matching_properties == len(property_names):
            filtered_tags.append(tag)
    return filtered_tags   

def extract_property_values(property, tags):
    property_values = []
    for tag in tags:
        if type(tag) != str:
            tag = str(tag)
        lst = tag.split(property+"=")
        if len(lst) == 1:
            continue
        value = lst[1][1:]
        value = value[:value.index("\"")]
        property_values.append(value)
    return property_values


def summarize(content: str, query: str, model="gpt-3.5-turbo", GAP=5000):
    resps = []
    for i in range(0, len(content), GAP):
        prompt = \
    """\
Your task will be to find and extract all content from a chunk of text related to the query:
\"\"\"\"\"\"
{query}
\"\"\"\"\"\"

Summarize this chunk of text or respond with the single string "NO_RELEVANT_CONTENT" if nothing related to the query is found:
\"\"\"\"\"\"
{content}
\"\"\"\"\"\"\
"""
        prompt = re.sub("{content}", content[i:i+GAP], prompt)
        prompt = re.sub("{query}", query, prompt)

        resp = prompt_gpt_3_5_turbo(prompt)
        if "NO_RELEVANT_CONTENT" in resp:
            continue

        resps.append(resp)
    return "\n".join(resps)

def get_search_result_links(query):
    query = re.sub("[^a-zA-Z| ]", "", query)
    query = re.sub(" +", "+", query)
    link = "https://www.google.com/search?q=" + query
    resp = requests.get(link)
    soup = BeautifulSoup(resp.text, "html.parser")
    anchor_tags = soup.find_all('a')
    anchor_tags = [at for at in anchor_tags if 'href="/url?q=' in str(at)]
    anchor_tags = list(map(str, anchor_tags))
    anchor_tags = ["".join(at.split('href="/url?q=')[1:]) for at in anchor_tags]
    search_result_links = [at[:at.find('&')] for at in anchor_tags]
    return search_result_links

def get_content_by_url(url, query):
    try:
        src = requests.get(url).text
    except:
        return ""
    text = parse_src_text(src)
    text = summarize(text, query)
    return text

def get_search_query_content(query):
    links = get_search_result_links(query)
    content = {}
    for link in links:
        content[link] = get_content_by_url(link, query)


    sqcontent = ""
    for k,v in content.items():
        sqcontent += f"{k}:\n"
        sqcontent += f'""""""\n{v}\n""""""\n\n'
    print("\n------------------> CONTENT FROM SEARCH QUERY:")
    print(sqcontent)
    return sqcontent.strip()

def search_query(query):
    return get_search_query_content(query)

def get_search_results(query):
    return json.dumps(get_search_result_links(query))









