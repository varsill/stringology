from queue import LifoQueue as Queue


class Node:
    def __init__(self, _parent, _char, _depth):
        self.parent = _parent
        self.children = {}
        self.letter = _char
        self.depth = _depth
        self.link = None

    def __str__(self, level=0):
        ret = "\t" * level + str(self.letter) + "\n"
        for key in self.children:
            ret += self.children[key].__str__(level + 1)
        return ret

    def find(self, label):
        node=self
        while len(label)!=1:
            node=node.children[label[0]]
            label=label[1:]
        return label in node.children


def terminate(text):
    dict = set()
    for char in text[:-1]:
        dict.add(char)
    if text[-1] in dict:
        for i in range(128, 255):
            if not chr(i) in dict:
                text = text+str(chr(i))
                return text
        raise Exception("All ASCII characters are in use in given text. Cannot find terminator.")
    return text


class Trie:

    def __init__(self, text):
        text = terminate(text)
        self.root = Node(None, None, 0)
        self.name = "Trie"
        self.naive_initialization(text)

    def naive_initialization(self, text):
        node = self.root
        depth = 1
        for char in text:
            node.children.update({char: Node(node, char, depth)})
            node = node.children[char]
            depth = depth+1

        for i in range(1, len(text)-1):
            self.add_suffix(text[i:])

    def add_suffix(self, suffix):
        head = self.get_head(suffix)
        node = head
        depth = head.depth+1
        for c in suffix[head.depth:]:
            node.children.update({c: Node(node, c, depth)})
            node = node.children[c]
            depth = depth + 1
    def find(self, label):
        return self.root.find(label)
    def __str__(self):
        return str(self.root)

    def get_head(self, suffix):
        node = self.root
        prev = None
        for c in suffix:
            if not node:
                return prev
            prev = node
            node = node.children.get(c, None)
        return prev







