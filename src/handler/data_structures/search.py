import re
from collections import Counter
from src.handler.parse.searching import simplify


class Infobit(object):
    def __init__(self, question="", answer=""):
        self.question = question
        self.answer = answer
        self.simplified = ""
        

class DataTable(object):

    def __init__(self, name):
        self.name = name
        self.pages = {}
        self.PageIndexer = {}
        self.IDX_LIMIT = 2
        self.N = 15

    def load(self, pages, posts=[]):
        # use pages as posts if not posts
        for idx, page in enumerate(pages):
            self.pages[idx] = posts[idx]
            words = simplify(page)
            words = words.split(" ")
            if not words:
                continue
            for block in range(1, self.N + 1, 1):
                for i in range(len(words)-block+1):
                    mystic = " ".join(words[i:i+block])
                    if mystic not in self.PageIndexer:
                        self.PageIndexer[mystic] = set({})
                    self.PageIndexer[mystic].add(idx)


    def deconstruct(self, n, lst, composition):
        if n < 1:
            return lst
        if n == 1:
            return lst
        for i in range(len(lst)-n+1):
            ngram = " ".join(lst[i:i+n])
            if ngram in self.PageIndexer:
                composition.append(ngram)
                composition = self.deconstruct(n-1, lst[:i], composition) + [ngram] + self.deconstruct(n, lst[i+n:], composition)
                return composition
        composition = self.deconstruct(n-1, lst, composition)
        return composition


    def reconstruct(self, composition):
        scoring = {}
        for comp in composition:
            if comp not in self.PageIndexer:
                continue
            for idx in self.PageIndexer[comp]:
                if idx not in scoring:
                    scoring[idx] = set({})
                scoring[idx].add(comp)
        return scoring

    def query(self, queryInput, cutt_off = 0.6):
        queryInput = queryInput.lower()
        # replace with simplify()
        queryInput = re.sub("[^a-zA-Z| ]", "", queryInput)
        queryInput = re.sub(" +", " ", queryInput).strip()
        
        query_words = queryInput.split(" ")
        query_word_count = len(query_words)
        composition = self.deconstruct(self.N, query_words, [])
        scoring = self.reconstruct(composition)
        
        mIdx, mScore = -1, -1
        for idx in scoring:
            score = len(scoring[idx])
            if score >= mScore:
                word_count = len(self.pages[idx].question.split(" "))
                if word_count / query_word_count <= cutt_off:
                    continue
                if score == mScore:
                    # less words
                    wca = len(self.pages[idx].simplified.split(" "))
                    wcb = len(self.pages[mIdx].simplified.split(" "))
                    if wca < wcb:
                        mIdx, mScore = idx, score    
                else:
                    mIdx, mScore = idx, score
        
        if mIdx == -1 or mScore == -1:
            return None
        
        return self.pages[mIdx]

    
    def query_multiple(self, queryInput):
        queryInput = queryInput.lower()
        queryInput = simplify(queryInput)
        words = queryInput.split(" ")

        composition = self.deconstruct(self.N, words, [])
        scoring = self.reconstruct(composition)

        scoring = dict(sorted(scoring.items(), key=lambda x: len(x[1])))
        
        return [result[1] for result in scoring[:min(len(scoring), 10)]]
    
    def one_norm(self, s1, s2):
        # put somewhere else
        s1, s2 = simplify(s1), simplify(s2)
        lst1, lst2 = s1.split(" "), s2.split(" ")
        dd1, dd2 = Counter(lst1), Counter(lst2)

        unique_words_matched = 0
        for key in list(Counter(lst1 + lst2).keys()):
            if key in dd1 and key in dd2:
                unique_words_matched += 1
        return unique_words_matched
