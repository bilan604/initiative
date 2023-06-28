import re
from bs4 import BeautifulSoup
from src.handler.parse.parsing import getTags, parse_text_spacing, get_uniform_spacing


def add_answers_to_dd(dd, tags):
    """
    This function locates parent tags for existing questions/labels and checks
    if there is a minimal parent tag
    that contains both the label and the input
    """
    def find_shortest_parent(q, qt, tags):
        m = ""
        ml = float('inf')
        for tag in tags:
            if qt in tag:
                if len(tag) < ml:
                    m = tag
                    ml = len(tag)
        return m


    qas = []
    tagsContainingInput = [tag for tag in tags if tag.count("<input ") == 1]
    print(f"{len(tagsContainingInput)=}\n")
    
    for key, val in dd.items():
        question, questionTag = val
        parentTag = find_shortest_parent(question, questionTag, tagsContainingInput)

        idx = parentTag.find("<input")
        input = parentTag[idx:]
        input = input[:input.find(">")+1]
        dd[key].append(input)
    
    for key in dd:
        # No answer identifier
        if len(dd[key]) != 3: continue
        # Empty answer identifier
        if not dd[key][-1]: continue
        # indicating a parent containing one input was found
        # ToDo: check that no other questions are in the 
        qas.append({
            "question": dd[key][0],
            "question_identifier": dd[key][1],
            "answer_identifier": dd[key][2]
            })
    return qas


def get_filtered_qas(qas):
    nonEmptyQAs = []
    for i in range(len(qas)):
        if re.sub("[^a-zA-Z]", "", qas[i]["question"]).strip():
            nonEmptyQAs.append(qas[i])
    qas = nonEmptyQAs

    filteredQAs = []
    for i in range(len(qas)):
        add = True
        for j in range(len(qas)):
            if i == j: continue
            if qas[j]["question"] in qas[i]["question"]:
                add = False
                break
        if not add:
            print("removing", qas[i]["question"])
            continue
        
        filteredQAs.append(qas[i])
    return filteredQAs


def question_answer_fast(id, bodyContent, filter_qas=False):
    # regarding filtered_qas = False by default: They have been filtered in answers
    tags = getTags(bodyContent)
    questions = {}
    for i, tag in enumerate(tags):
        if len(tag) > 100000: continue
        
        words = parse_text_spacing(tag)
        words = get_uniform_spacing(words)
        if 1 <= len(words) < 20:
            if words not in questions:
                questions[words] = [tag, i]
            else:
                if len(questions[words][0]) > len(tag):
                    questions[words] = [tag, i]
    
    # Map<int, Array<str>>: Indexes of tags, and array of tag identifiers from the html
    dd = {}
    # Duplicate question checker
    appearances = {} 

    for question, questionHTML in questions.items():
        if question not in appearances:
            appearances[question] = 1
        else:
            appearances[question] += 1
    for question, questionHTML in questions.items():
        if appearances[question.strip()] > 1:
            continue            
        dd[questionHTML[1]] = [question, questionHTML[0]]
        print("questions:", question)
    qas = add_answers_to_dd(dd, tags)
    if filter_qas:
        qas = get_filtered_qas(qas)

    # remove answer_identifiers appearing more than once
    return qas
