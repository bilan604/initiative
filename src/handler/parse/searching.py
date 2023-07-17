import re
from src.handler.parse.parsing import *

def replace(a, b, c):
    return re.sub(a, b, c)

def parse_answer_key(answer_key):
    answer_key = re.sub("[^a-zA-Z]", " ", answer_key)
    answer_key = parse_text_spacing(answer_key).lower()
    return answer_key

def simple(sent):
    sent = sent.lower().strip()
    sent = re.sub("[\'|\-]", " ", sent)
    sent = re.sub("[^a-zA-Z]", " ", sent)
    sent = re.sub(" +", " ", sent)
    sent = sent.strip()
    return sent


def simplify(s):
    return simple(s)
