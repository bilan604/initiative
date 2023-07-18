from math import sqrt
from collections import Counter


# Google these days uses (on paper)
# Map {word: [idx of sentences that contains the word]}

# which I includes this (on paper)

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

