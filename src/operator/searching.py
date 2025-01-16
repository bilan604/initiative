import re
import requests
from bs4 import BeautifulSoup
from collections import Counter
from src.handler.parser import *


def prompt_auto_auto(query):
    return "PLC functionality removed until auth is added"

def get_url_results(url: str) -> list[str]:
    resp = requests.get(url)
    urls = []
    soup = BeautifulSoup(resp.text, "html.parser")
    for a in list(map(str, soup.find_all('a'))):
        a = a[:a.find(">")+1]
        props = getProperties(a)
        href = "" if "href" not in props else re.sub("&amp;", "", props["href"])
        if href.find("/url?q=") == 0:
            href = href[len("/url?q="):]
            idx = href.find("&")
            if idx != -1:
                href = href[:idx]

            if "youtube" in href:
                href = re.sub("%3F", "?", href)
                href = re.sub("%3D", "=", href)
            
            
            urls.append(href)
    return urls

def google_search_page(query, start: str):
    query = "+".join(query.split(" "))
    url = f"https://www.google.com/search?q={query}"
    if start:
        url += f"&start={start}"
    results = get_url_results(url)
    return results

def google_search(query):
    return google_search_page(query, "")

def get_search_result_links(query):
    return google_search(query)

def google_search_pages(query: str, n: int) -> list[int]:
    # Goes through pages until n results
    if type(n) == str:
        n = int(n)
    if n <= 0:
        return []
    if n >= 100:
        n = 100
    vis = {}
    # assuming 12 per page...
    for start in range(0, n * (30 // 10) + 1, 20):
        urls = google_search_page(query, str(start))

        for url in urls:
            if url.find('https://support.google.com/websearch') == 0:
                continue
            if url.find('https://accounts.google.com/ServiceLogin') == 0:
                continue
            if url not in vis:
                vis[url] = 1
            else:
                vis[url] += 1
        
        if len(vis) >= n:
            return list(set(list(vis.keys())))
    
    return list(set(list(vis.keys())))

def test_queries():
    # It doesn't return a lot of urls. Understandable. Imitation game.
    
    # const
    search_queries = [
        "How to learn Python programming",
        "Best books on machine learning",
        "Healthy breakfast recipes",
        "New York City tourist attractions",
        "Latest smartphones 2023",
        "Climate change effects on ecosystems",
        "SpaceX rocket launches schedule",
        "DIY home improvement projects",
        "Top 10 action movies of all time",
        "Weather forecast for Paris",
        "Historical events of the 20th century",
        "Beginner's guide to gardening",
        "Famous quotes about success"
    ]
    s = 0
    for q in search_queries:
        urls = google_search_pages(q, 20)
        if len(urls) >= 20:
            s += 1

