import re

def minDistance(word1: str, word2: str) -> int:
    word1 = "-" + word1
    word2 = "-" + word2
    m = len(word1)
    n = len(word2)

    # Initialize the dp table
    dp = [[0] * (n) for _ in range(m)]

    # Base cases
    for i in range(m):
        dp[i][0] = i
    for j in range(n):
        dp[0][j] = j

    # Fill in the dp table
    for i in range(1, m):
        for j in range(1, n):
            if word1[i] == word2[j]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j-1], dp[i][j-1], dp[i-1][j])
    return dp[m-1][n-1]

def matchOptionStrings(answer: str, optionStrings: list[str]):
    """
    answer: the ideal answer for some given question
    optionStrings: the answers to select from
    """
        
    def simplify(s: str):
        # converts HTML code to uniformly spaced lowercase letters (words)
        # note: some text may be white on the webpage
        if type(s) != str:
            return ""
        s = s.lower()
        s = re.sub("[^a-zA-Z|0-9|\-|\%| ]", " ", s)
        s = re.sub(" +", " ", s)
        s = s.strip()
        return s

    bestIdx = -1
    bestOption = -1
    bestScore = -1
    for i in range(len(optionStrings)):
        # opt? :o
        option = optionStrings[i]
        a = simplify(answer)
        b = simplify(option)
        dist = minDistance(a, b)
        n = max(len(a), len(b))
        if n == 0:
            score = -1
            continue
        else:
            score = 1-(dist/n)
        
        if score >= bestScore:
            bestIdx = i
            bestScore = score
            bestOption = option
    
    if bestScore == -1:
        return None
    return bestOption, bestIdx