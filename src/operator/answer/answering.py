import numpy as np
import pandas as pd
from src.operator.loader.data_loading import load_question_data
from src.handler.parse.parsing import parseAnswerTextSpacing


def checkAnsweredQuestions(pageQuestion, answeredQuestions):
        for answeredQuestion in answeredQuestions:
            if answeredQuestion.find(pageQuestion) == 0:
                # and/or other specifications
                return answeredQuestion
        return None

#### placeholder for data retrieval/recieving endpoint
def load_question_data_plc(userId):
    questionData = {}
    df = pd.read_csv("src/operator/answer/"+userId+".txt")
    mtx = np.array(df)
    for i in range(len(mtx)):
        row = [ij for ij in list(mtx[i,:]) if str(ij).lower() != "nan"]
        questionData[row[0]] = []
        for j in range(1, len(row)):
            questionData[row[0]] += [row[j]]
    return questionData


def answer_input_questions(id, inputQuestions):
    
    
    ##########
    # placeholder implementation
    def check_keynames(input_question):
        if len(input_question) == 3:
            if "question" in input_question and "question_identifier" in input_question and "answer_identifier" in input_question:
                return True
        return False

    # filter by checking the names of the keys are correct
    inputQuestions = [input_question for input_question in inputQuestions if check_keynames(input_question)]

    # @alex replace the following implementation with the component you need to connect this to

    def get_sample_data(inputQuestions):
        sample_data = {}
        for input_question in inputQuestions:
            sample_data[input_question["question"].lower()] = "answer for " + input_question["question"].lower()
        return sample_data
    
    # This is just a hashmap
    sample_data_for_id = get_sample_data(inputQuestions)
    
    # replace this hashmap direct match with the appropriate implementation
    answered_questions = []
    for question in inputQuestions:
        hashmap_key = question["question"].lower()
        if hashmap_key in sample_data_for_id:
            sample_data_for_id[hashmap_key]
            answered_question = question.copy()
            answered_question["answer"] = sample_data_for_id[hashmap_key]
            answered_questions.append(answered_question)
    return answered_questions