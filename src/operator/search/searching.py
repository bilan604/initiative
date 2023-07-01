import re
import requests
from bs4 import BeautifulSoup


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