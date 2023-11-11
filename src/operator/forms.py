import re
import string
import requests
from bs4 import BeautifulSoup
from src.handler.parser import *


# call get method to request that page 
def get_pathed_questions(url: str) -> dict[tuple, dict]:
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    body = soup.find('body')

    def get_opening_tag(src):
        for i in range(len(src)):
            if src[i] == ">":
                return src[:i+1]
        return ""

    def get_element_type(src):
        ot = get_opening_tag(src)
        letters = string.ascii_letters
        ans = ""
        for i in range(1, len(ot)):
            if ot[i] not in letters:
                return ans
            ans += ot[i]
        return ans

    target_elements = ['input', 'textarea', 'select']
    def recu(e, path, dd):
        e_type = get_element_type(str(e)).lower()
        if e_type == 'script':
            return
        if e_type in target_elements:
            key = tuple(path)
            dd[key] = e
            return
        if str(type(e)) == "<class 'bs4.element.Tag'>":
            children = list(e.children)
        else:
            children = []
        
        for i, child in enumerate(children):
            recu(child, path + [i], dd)
        return dd
    
    dd = recu(body, [], {})

    def get_question(e):
        src = str(e)
        s = str(src)
        s = re.sub("\n", " ", s)
        s = re.sub(" +", " ", s)
        s = re.sub("<.+?>", "\n", s)
        s = s.strip()
        if not s:        
            return get_question(e.parent)
        return s
    
    def get_select_question(e):
        src = str(e)
        options = BeautifulSoup(src, 'html.parser').find_all('option')
        options = list(map(str, options))
        option_texts = [getText(option).strip() for option in options]
        
        def get_filtered_text(src: str, option_texts: list[str]) -> str:
            s = re.sub("\n", " ", src)
            s = re.sub(" +", " ", s)
            s = re.sub("<.+?>", "\n", src)
            s = s.strip()
            lst = s.split("\n")
            lst = [item for item in lst if getText(item).strip() and getText(item).strip() not in option_texts]
            if not lst:
                return ""
            new_s = "\n".join(lst)
            return new_s

        element = e
        filtered_e = get_filtered_text(str(element), option_texts)
        for i in range(10):  # limit 10
            if filtered_e:
                return filtered_e
            element = e.parent
            filtered_e = get_filtered_text(str(element), option_texts)

        return "NONE"



    def convert_element_to_question(e):
        
        tag = str(e)
        e_type = get_element_type(str(e)).lower()
        if e_type == "textarea":
            question_str = get_question(e)
        # not necessarily inputs, because mc inputs
        if e_type == "input":
            question_str = get_question(e)
        if e_type == "select":
            question_str = get_select_question(e)

        answerOptions = []
        """
        if e_type == "textarea":
            answerOptions = [tag]
        if e_type == "input":
            properties = getProperties(tag)
            if 'type' in properties:
                e_type = properties['type']
                # except checkbox
                answerOptions = [tag]
            else:
                answerOptions = [tag]
        """
        if e_type == "select":
            options = BeautifulSoup(tag, 'html.parser').find_all('option')
            options = list(map(str, options))
            answerOptions = [[getText(option), option] for option in options]

        question = {
            'question': question_str,
            'tag': tag,
            'type': e_type,
            # answerOptions defaults to the tag
            'answerOptions': answerOptions,
        }
        return question

    def check_question(q: str, qs: str) -> bool:
        # checks if the question is made of multiple other questions
        # return true if it is NOT a question
        if q.count("\n") >= 6:
            return True
        q = q.strip()
        count = 0
        for qsi in qs:
            qsi = qsi.strip()
            if qsi == q:
                continue
            if len(qsi) >= 2 and qsi in q:
                count += 1
        if count >= 2:
            return True
        return False

    questions = {}
    for path, e in dd.items():
        question = convert_element_to_question(e)
        questions[path] = question
    
    remove_questions = []
    question_strings = [question['question'] for question in questions.values()]
    for path, question in questions.items():
        isnt_question = check_question(question['question'], question_strings)
        if isnt_question:
            remove_questions.append(path)
    
    questions = {path: question for path, question in questions.items() if path not in remove_questions}
    
    return questions

def get_questions(url: str) -> list[dict]:
    # note: answerOptions is empty on default here, which is not
    # the case with internetAgent
    pathed_questions = get_pathed_questions(url)
    questions = list(pathed_questions.values())
    return questions
