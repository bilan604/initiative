

def multi_prompt(text, src, url=""):
    if url:
        multi_prompt = f'This is the html content from {url}:\n”””\n{src}\n”””\n\n'
    else:
        multi_prompt = f'Here is the html content from a element in a webpage:\n”””\n{src}\n”””\n\n'
    
    multi_prompt += f'The text rendered onto the webpage from the content is:\n“””\n{text}\n“””\n\n'
    multi_prompt += f'You must determine whether the text contains at least one user-input-question. A user-input-question MUST contain two things:\n'
    multi_prompt += f'1. The HTML content must contain the text for the label/question(s), or a text label for the question(s) such as a <span> tag.\n'
    multi_prompt += f'2. The HTML content must contain the tag for user input corresponding to the question, such as an <input> tag.\n\n'
    multi_prompt += f'Some examples of questions are “First Name”, “Carrier Booking Ref*”, “Color”, “License No”, and “Name*”. If there is no user-input-question or if the user-input-question does not meet BOTH requirements, respond with either “FALSE:NO QUESTION” or “FALSE:INCOMPLETE QUESTION”.\n'
    multi_prompt += f'Otherwise, respond with “TRUE:” followed immediately by a JSON object containing the user-input-questions. The keys for each user-input-question will be “question”, “question_identifier”, and “answer_identifier”. The identifiers are the opening tag for the corresponding element. '
    multi_prompt += f'When selecting an html opening tag for the question or answer identifier, make sure to select an opening tag with a unique attribute key:value pair such as id="CommercialMastersAddCargoModal" or class="ta-creative__description".\n'
    multi_prompt += \
"""
Example Response: 'TRUE:[{“question”: “Email Address”,“question_identifier”: “<span class="M7eMe">Email Address</span>”,“answer_identifier”: “<input type="text" class="whsOnd zHQkBf" jsname="YPqjbf" autocomplete="off" tabindex="0" aria-labelledby="i1" aria-describedby="i2 i3" dir="auto" data-initial-dir="auto" data-initial-value="">”},{“question”: “Prod. Date”,“question_identifier”: “<span style="white-space:pre-wrap">Prod. Date</span>”,“answer_identifier”: “<input type="text" class="whsOnd zHQkBf" jsname="YPqjbf" autocomplete="off" tabindex="0" aria-labelledby="i101" aria-describedby="i102 i103" dir="auto" data-initial-dir="auto" data-initial-value="">”}]'
"""
    return multi_prompt