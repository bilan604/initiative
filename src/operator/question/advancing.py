import re
import tiktoken
from bs4 import BeautifulSoup
from src.handler.parse.parsing import load_response, get_text
from src.handler.prompt.prompting import multi_prompt
from src.operator.ai.openai import askGPT4


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


def question_answer_prompts(id, src, threshold=100):
    """
    Generates prompts for extracting HTML content
    """

    def subsetOfVisitedTags(tag, visitedTags):
        for visitedTag in visitedTags:
            if tag in visitedTag:
                return True
        return False

    enc = tiktoken.encoding_for_model('gpt-4')
    
    prompts = []

    soup = BeautifulSoup(src, 'html.parser')
    tags = soup.find_all()
    tags = list(map(str, tags))
    tags = sorted(tags, key=lambda x: len(x), reverse=True)
    
    visited = set({})
    visitedTags = set({})
    for tag in tags:
        text = get_text(tag)

        # Skip when element does not contain <input> child node
        if "input" not in tag:
            continue
        # Skip when there is no text present at all
        if not text:
            continue
        if len(enc.encode(text)) > threshold:
            continue
        prompt = multi_prompt(text, tag)

        # Very high upper bound
        if len(enc.encode(prompt)) > 1000:
            continue
        # works only when sorted in reverse
        # otherwise, this will skip context
        if text in visited:
            continue
        visited.add(text)
        if subsetOfVisitedTags(tag, visitedTags):
            continue
        visitedTags.add(tag)
        prompts += [prompt]
    
    return prompts


def contentualize(responses, context_target="question"):
    counts = {}
    for resp_obj in responses:
        for qa in resp_obj:
            if qa[context_target] not in counts:
                counts[qa[context_target]] = 0
            counts[qa[context_target]] += 1
    
    ans = []
    for resp_obj in responses:
        unique = []
        duplicated = []
        for qa in resp_obj:
            if counts[qa[context_target]] == 1:
                unique.append(qa)
            else:
                duplicated.append(qa)
        if duplicated:
            if unique:
                context = "(" +" ".join([uqa[context_target] for uqa in unique]) + ") "
            else:
                context = ""
            for i in range(len(duplicated)):
                duplicated[i][context_target] = context + duplicated[i][context_target]
            ans += unique + duplicated
        else:
            if not duplicated and not unique:
                continue
            if duplicated:
                print("Duplicates with no context recieved")
            elif unique:
                ans += unique
    return ans

def question_answer_prompting(identifier, prompts):
    # identifier is openai key for now
    if not identifier:
        return "No identifier"

    # list of list question answers
    responses = []
    visited_questions = {}
    for query_prompt in prompts:
        response = askGPT4(identifier, query_prompt)
        if not response:
            continue
        if response.find("TRUE:") == -1:
            continue
        response_object = load_response(response)
        if not response_object:
            continue
        responses.append(response_object)
    
        print(responses)
        print("responses:------------\n\n")
    
    responses = contentualize(responses, "question")
    print(responses)
    print("responses:------------\n\n")
    return responses




