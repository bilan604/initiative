from src.handler.parse.asking import *


"""
This was to automate job applications
"""


def get_click_input_labels(inputs, elements):
    """
    finds labels for some click inputs, elements come before the inputs in size
    so it will not contain a superset of the question
    """
    labels = []
    for input in inputs:
        for element in elements:
            if len(element) > len(input) and input in element:
                text = get_spaced_words(element)
                if text:
                    labels.append(text)
                    break
    return labels


def parse_answer_key(answer_key):
    answer_key = re.sub("[^a-zA-Z]", " ", answer_key)
    answer_key = parse_text_spacing(answer_key).lower()
    return answer_key


def get_questions(src, properties_rule):
    """
    i.e. properties_rule=lambda x: class in x and x[class] == 'question-list-element'

    This function takes the src (innerHTML) of the container element for all the questions
    Properties rule is a rule that is used to specified a container for the question that is matched
    with a dictionary like {"class": "question-list-element"}.
    """
    questions = []
    elements = get_elements_by_src(src, "")
    elements = sorted(elements, key=lambda x: len(x))
    for i, element in enumerate(elements):
        if len(element) > 50000:
            continue

        opening_tag = get_opening_tag(element)
        properties = get_properties(opening_tag)

        # This will filter out everything that isnt a question actually.
        if not properties_rule(properties):
            continue
        
        # This is LinkedIn specific
        element_text = get_spaced_words(element)
        
        if not element_text:
            continue
        if element.find("<input") == -1 and element.find("<option") == -1:
            continue

        element_texts = get_text(element).strip().split("\n")

        inputs = get_elements_by_src(element, "input")
        input_text = [parse_text_spacing(get_text(input)) for input in inputs]
        input_text = [it for it in input_text if it]

        options = get_elements_by_src(element, "option")
        option_text = [parse_text_spacing(get_text(option)) for option in options]
        option_text = [ot for ot in option_text if ot]

        question = element_texts[0]
        
        if len(inputs) == 1:
            # its text input
            # answer_options is the LITERAL TEXT
            questions.append({
                "question": question,
                "question_tag": opening_tag,
                "answer_elements": inputs,
                "answer_options": [],
                "type": "text-input",
                "question_element": element
            })
        else:
            if len(inputs) > 1:
                questions.append({
                    "question": question,
                    "question_tag": opening_tag,
                    "answer_options": get_click_input_labels(inputs, elements[:i]),
                    "answer_elements": inputs,
                    "type": "multiple-inputs",
                    "question_element": element
                })
            else:
                # is options, a select
                questions.append({
                    "question": question,
                    "question_tag": opening_tag,
                    "answer_options": option_text,
                    "answer_elements": options,
                    "type": "select",
                    "question_element": element
                })

    return questions

