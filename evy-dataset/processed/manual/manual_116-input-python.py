class Node:
    def __init__(self):
        self.next = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.data = Node()

    def insert(self, word: str) -> None:
        node = self.data
        for ch in word:
            if ch not in node.next:
                node.next[ch] = Node()
            node = node.next[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.data
        for ch in word:
            if ch not in node.next:
                return False
            node = node.next[ch]
        return node.is_end

    def startsWith(self, prefix: str) -> bool:
        node = self.data
        for ch in prefix:
            if ch not in node.next:
                return False
            node = node.next[ch]
        return True

def test():
    trie = Trie()
    trie.insert("apple")
    assert(trie.search("apple"))
    assert(not trie.search("app"))
    assert(trie.startsWith("app"))
    trie.insert("app")
    assert(trie.search("app"))

test()

