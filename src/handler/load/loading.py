import pandas as pd
from src.handler.parse.searching import simplify, replace
from src.handler.data_structures.search import Infobit, DataTable


def load_information(id, csv_name="tester_info"):
    # since its a dataframe, this component is replaceable with google sheets
    if ".csv" in csv_name:
        csv_name = replace(".csv", "", csv_name)
    
    path = f"src/storage/{id}/{csv_name}.csv"
    
    df = pd.read_csv(path)
    print("\ndf:", df)

    questions = list(df["Question"])
    answers = list(df["Answer"])

    infos = [Infobit(q,a) for q,a in zip(questions,answers)]
    for i in range(len(infos)):
        infos[i].simplified = simplify(infos[i].question)
    return questions, infos