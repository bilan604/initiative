
import re
import requests
from bs4 import BeautifulSoup
from src.handler.math.cosine_similarity import *
from timeit import default_timer


def get_pages(links):
    pages = []
    for link in links:
        s = requests.get(link).text
        soup = BeautifulSoup(s)
        p_tags = soup.find_all("p")
        pageToAdd = [re.sub("[\<.*\>|\n]", "", p.text.lower()) for p in p_tags]
        pageToAdd = [re.sub("[^a-z| ]", "", p) for p in pageToAdd if len(p) > 15]
        pages += [" ".join(pageToAdd)]
    return pages


def bench_mark_test():
    links = ['https://developers.google.com/machine-learning/clustering/similarity/measuring-similarity?hl=ko', 'https://developers.google.com/machine-learning/clustering/similarity/measuring-similarity?hl=pl', 'https://developers.google.com/machine-learning/clustering/similarity/measuring-similarity?hl=pt-br', 'https://developers.google.com/machine-learning/clustering/similarity/measuring-similarity?hl=ru', 'https://developers.google.com/machine-learning/clustering/similarity/measuring-similarity?hl=es-419', 'https://developers.google.com/machine-learning/clustering/similarity/measuring-similarity?hl=th', 'https://developers.google.com/machine-learning/clustering/similarity/measuring-similarity?hl=tr', 'https://developers.google.com/machine-learning/clustering/similarity/measuring-similarity?hl=vi', 'https://developers.google.com/machine-learning/clustering/similarity/measuring-similarity', 'https://developers.google.com/machine-learning', 'https://developers.google.com/machine-learning/clustering/similarity/measuring-similarity', 'https://developers.google.com/machine-learning', 'https://developers.google.com/machine-learning/foundational-courses', 'https://developers.google.com/machine-learning/foundational-courses', 'https://developers.google.com/machine-learning/advanced-courses', 'https://developers.google.com/machine-learning/advanced-courses', 'https://developers.google.com/machine-learning/guides', 'https://developers.google.com/machine-learning/guides', 'https://developers.google.com/machine-learning/glossary', 'https://developers.google.com/machine-learning/glossary', 'https://developers.google.com/machine-learning/glossary', 'https://developers.google.com/machine-learning/glossary', 'https://developers.google.com/machine-learning/glossary', 'https://developers.google.com/machine-learning/glossary/clustering', 'https://developers.google.com/machine-learning/glossary/clustering', 'https://developers.google.com/machine-learning/glossary/df', 'https://developers.google.com/machine-learning/glossary/df', 'https://developers.google.com/machine-learning/glossary/fairness', 'https://developers.google.com/machine-learning/glossary/fairness', 'https://developers.google.com/machine-learning/glossary/fundamentals', 'https://developers.google.com/machine-learning/glossary/fundamentals', 'https://developers.google.com/machine-learning/glossary/googlecloud', 'https://developers.google.com/machine-learning/glossary/googlecloud', 'https://developers.google.com/machine-learning/glossary/image', 'https://developers.google.com/machine-learning/glossary/image', 'https://developers.google.com/machine-learning/glossary/language', 'https://developers.google.com/machine-learning/glossary/language', 'https://developers.google.com/machine-learning/glossary/recsystems', 'https://developers.google.com/machine-learning/glossary/recsystems', 'https://developers.google.com/machine-learning/glossary/rl', 'https://developers.google.com/machine-learning/glossary/rl', 'https://developers.google.com/machine-learning/glossary/sequence', 'https://developers.google.com/machine-learning/glossary/sequence', 'https://developers.google.com/machine-learning/glossary/tensorflow', 'https://developers.google.com/machine-learning/glossary/tensorflow', 'https://developers.google.com/s/results/machine-learning', 'https://developers.google.com/s/results', 'https://developers.google.com/machine-learning/advanced-courses', 'https://developers.google.com/machine-learning', 'https://developers.google.com/machine-learning', 'https://developers.google.com/machine-learning/clustering', 'https://developers.google.com/machine-learning/clustering', 'https://developers.google.com/machine-learning', 'https://developers.google.com/', 'https://developers.google.com/products', 'https://developers.google.com/machine-learning', 'https://developers.google.com/machine-learning/advanced-courses', 'https://developers.google.com/machine-learning/clustering', 'https://developers.google.com/site-policies', 'https://developers.google.com/', 'https://developers.google.com/machine-learning/crash-course/embeddings/video-lecture', 'https://developers.google.com/machine-learning/recommendation/collaborative/basics', 'https://developers.google.com/machine-learning/recommendation', 'https://developers.google.com/machine-learning/recommendation/overview/candidate-generation#which-similarity-measure-to-choose', 'https://developers.google.com/machine-learning/recommendation/collaborative/basics', 'https://developers.google.com/machine-learning/crash-course/embeddings/video-lecturehttps://developers.google.com/machine-learning/recommendation/collaborative/basicshttps://developers.google.com/machine-learning/recommendationhttps://developers.google.com/machine-learning/recommendation/overview/candidate-generation#which-similarity-measure-to-choosehttps://developers.google.com/machine-learning/recommendation/collaborative/basics']
    pages = get_pages(links)
    
    indexes = getMap(pages)
    pageSizes = getSizeOfPage(pages)
    
    a,b = 0.0, 0.0
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
            print(f"My calculation {val1} took:", (end-start)*1000, "seconds")
            a += (end-start)*1000
            start = default_timer()
            val2 = cosineSimilarityDoubleCheck(query, pages[pageIdx])
            end = default_timer()
            print(f"Default calculation {val2} took:", (end-start)*1000, "seconds")
            print(val2)
            b += (end-start)*1000
            
            print("\nThe cosine similarity score I calculated:", cosineSimilarity(query, pages[pageIdx]))
            print("The cosine similarity score by traditional calculation:", cosineSimilarityDoubleCheck(query.lower().split(), pages[pageIdx].lower().split()))
        print("-------------------------------\n")

    print("Total time using my optimization:", a)
    print("Total time traditional:", b)
    return
