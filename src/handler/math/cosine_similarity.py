from math import sqrt
from collections import Counter


# This is a constant time cosine similarity score algorithm
# I believe this is the same optimization method Google Search uses


# On init
def getMap(pages):
    dd = {}
    for i, sentence in enumerate(pages):
        for word in sentence.split(" "):
            if word not in dd:
                dd[word] = []
            dd[word].append(i)
    return dd
# On init
def getSizeOfPage(pages):
    dd = {}
    for i in range(len(pages)):
        dd[i] = sqrt(sum([val ** 2 for val in list(Counter(pages[i].split(" ")).values())]))
    return dd
# On init
def getRelevantPages(map, query):
    indexCounts = {}
    for word in query.split(" "):
        if word in map:
            for idx in map[word]:
                if idx not in indexCounts:
                    indexCounts[idx] = []
                indexCounts[idx] += [word]
    return indexCounts
# On init
def getPageCounts(pages):
    return [Counter(page.split(" ")) for page in pages]


## A^{10**9 x 14,000}x^{14,000 x 1}
def scoreSearchResults(searchResults, query, pageCounts, pageSizes):
    queryCounts = Counter(query.split(" "))
    queryLength = sqrt(sum([val**2 for val in list(queryCounts.values())]))
    cosineSimilarityScores = {}
    for pageIndex in searchResults:
        total = 0
        vis = set({})
        for pageWord in searchResults[pageIndex]:
            # hacky fix for proper ai*bi and not ai*bi + ai*bi
            if pageWord not in vis:
                vis.add(pageWord)
            total += pageCounts[pageIndex][pageWord] * queryCounts[pageWord]
        cosineSimilarityScores[pageIndex] = total / (pageSizes[pageIndex] * queryLength)
    return cosineSimilarityScores
  
# function to show that it is the same
def cosineSimilarity(words1, words2):
    c1 = Counter(words1.split(" "))
    c2 = Counter(words2.split(" "))
    top = 0
    for word in c1:
        if word in c2:
            top += c1[word] * c2[word]
    bottom = sqrt(sum([val**2 for val in c1.values()]))*sqrt(sum([val**2 for val in c2.values()]))
    return top/bottom

# another function to show that it is the same
def cosineSimilarityDoubleCheck(words1, words2):
    # Note that the items have been parsed already for cosine similarity score
    # Giving it a time advantage

    # universe = words1 + words2
    uniqueWords = list(set(words1 + words2))
    vectorizer = {uniqueWords[i]: i for i in range(len(uniqueWords))}
    vec1 = [0] * len(uniqueWords)
    vec2 = [0] * len(uniqueWords)
    for word in words1:
        vec1[vectorizer[word]] += 1
    for word in words2:
        vec2[vectorizer[word]] += 1
    return sum([a*b for a,b in zip(vec1, vec2)]) / (sqrt(sum([val**2 for val in vec1])) * sqrt(sum(val**2 for val in vec2)))


"""
# Benchmark


import re

import requests
from bs4 import BeautifulSoup

pages = []
links = ["https://developers.google.com/machine-learning/clustering/similarity/measuring-similarity", "https://cloud.google.com/blog/topics/developers-practitioners/find-anything-blazingly-fast-googles-vector-search-technology"]

for link in links:
    s = requests.get(link).text
    soup = BeautifulSoup(s)
    p_tags = soup.find_all("p")
    pageToAdd = [re.sub("[\<.*\>|\n]", "", p.text.lower()) for p in p_tags]
    pageToAdd = [re.sub("[^a-z| ]", "", p) for p in pageToAdd if len(p) > 15]
    pages += [" ".join(pageToAdd)]

indexes = getMap(pages)
pageSizes = getSizeOfPage(pages)
print(pageSizes)

from timeit import default_timer
pageCounts = getPageCounts(pages)
for query in ['dot product for vectors', "traditional search versus vector search"]:
    print("New query:", query)
    searchResults = getRelevantPages(indexes, query)
    pageScores = scoreSearchResults(searchResults, query, pageCounts, pageSizes)
    print(f"The cosine similarity scores calculated between the query and each page are:\n{pageScores}")
    for i, pageIdx in enumerate(list(searchResults.keys())):
        start = default_timer()
        val1 = cosineSimilarity(query, pages[pageIdx])
        end = default_timer()
        print("My calculation took:", (end-start)*1000, "seconds")
        start = default_timer()
        val2 = cosineSimilarityDoubleCheck(query, pages[pageIdx])
        end = default_timer()
        print("Default calculation took:", (end-start)*1000, "seconds")
        
        print("\nThe cosine similarity score I calculated:", cosineSimilarity(query, pages[pageIdx]))
        print("The cosine similarity score by traditional calculation:", cosineSimilarityDoubleCheck(query.lower().split(), pages[pageIdx].lower().split()))
    print("-------------------------------\n")
"""