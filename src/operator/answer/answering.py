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

    # replace the following implementation with whichever service/backend this needs to be connnected to:






    questionData = load_question_data_plc(id)
    print("questionData", questionData)
    if not questionData:
        return "No information found for id " + id

    def getAnsweredQuestions(questionData):
        # points to the input question to retrieve it
        pointer = {}
        for answer, question_synonyms in questionData.items():
            for question in question_synonyms:
                # parse the spacing for pointers to the answer, i.e. "full name"
                question = parseAnswerTextSpacing(question)
                pointer[question] = answer
        return pointer

    # Helper func to make retriever
    answeredQuestions = getAnsweredQuestions(questionData)
    matchedQuestions = []
    for inputQuestion in inputQuestions:
        # ToDo: add webpag support for questions formatted as synonym1/synonym2
        pageQuestion = inputQuestion["question"]
        pageQuestion = parseAnswerTextSpacing(pageQuestion)
        if pageQuestion in answeredQuestions:
            matchedQA = inputQuestion.copy()
            matchedQA["answer"] = answeredQuestions[pageQuestion]
            matchedQuestions.append(matchedQA)
        else:
            relevantQuestion = checkAnsweredQuestions(pageQuestion, answeredQuestions)
            if not relevantQuestion: continue
            matchedQA = inputQuestion.copy()
            matchedQA["answer"] = answeredQuestions[relevantQuestion]
            matchedQuestions.append(matchedQA)

    # filter out answer_identifiers with multiple appearances
    memo = {}
    for mq in matchedQuestions:
        if mq["answer_identifier"] not in memo:
            memo[mq["answer_identifier"]] = 1
        else:
            memo[mq["answer_identifier"]] += 1

    matchedQuestions = [mq for mq in matchedQuestions if memo[mq["answer_identifier"]] == 1]

    # filter out question_identifiers with multiple appearances
    memo = {}
    for mq in matchedQuestions:
        if mq["question_identifier"] not in memo:
            memo[mq["question_identifier"]] = 1
        else:
            memo[mq["question_identifier"]] += 1
    matchedQuestions = [mq for mq in matchedQuestions if memo[mq["question_identifier"]] == 1]
    return matchedQuestions

