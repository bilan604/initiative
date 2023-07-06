class TrieNode(object):
    def __init__(self, val, content="", children={}):
        self.val = val
        self.content = content
        self.children = children

