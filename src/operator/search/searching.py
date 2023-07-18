import re
import requests
from bs4 import BeautifulSoup
from collections import Counter
from src.handler.load.loading import load_information
from src.handler.data_structures.search import Infobit, DataTable


def get_datatable(id, table_name):
    datatable = DataTable(id)
    pagesA, postsA = load_information(id, table_name)
    datatable.load(pagesA, postsA)
    return datatable


def query_datatable(query, datatable):
    infobit = datatable.query(query)  #info = INPUTS.query(answer_key)
    answer = str(infobit.answer)
    return answer


# webscrapes google search, unrelated, should move
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



