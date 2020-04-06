class Node(object):

    def __init__(self, text):
        self.children = {}
        self.parent = None
        self.suffix_link = None
        self.start_index = 0
        self.end_index = 0
        self.text = text

    def graft(self, start_index, end_index):
        child = Node(self.text)
        self.children[self.text[start_index]] = child
        child.start_index = start_index
        child.end_index = end_index
        child.parent = self
        return child

    def break_node(self, where_to_break_node):
        assert where_to_break_node > self.start_index
        if where_to_break_node == self.end_index: return
        child = Node(self.text)
        child.start_index = self.start_index
        child.end_index = where_to_break_node
        child.parent = self.parent
        child.parent.children[child.text[self.start_index]] = child
        self.start_index = where_to_break_node
        self.parent = child
        child.children[self.text[where_to_break_node]] = self

    def length(self):
        return self.end_index - self.start_index

    def __str__(self, level=0):
        ret = "\t" * level + str(self.text[self.start_index:self.end_index]) + "\n"
        for key in self.children:
            ret += self.children[key].__str__(level + 1)
        return ret

    def label(self):
        return self.text[self.start_index: self.end_index]

    def find(self, label):
        if len(label) <= self.length():
            return label == self.label()[:len(label)]
        if label[:self.length()] != self.label():
            return False
        label = label[self.length():]
        if label[0] in self.children:
            return self.children[label[0]].find(label)
        return False

def slowfind(node, start_index, end_index):
    assert node is not None
    assert start_index <= end_index
    if start_index == end_index:
        return node, node
    text = node.text
    i = 0

    next = node.children.get(text[start_index])
    if next is None:
        leaf = node.graft(start_index, end_index)
        return node, leaf
    node=next
    while start_index < end_index:
        if node.start_index + i < node.end_index:
            if text[start_index] == text[node.start_index + i]:
                i += 1
                start_index += 1
            else:
                break
        else:
            i = 0
            next = node.children.get(text[start_index])
            if next is None:
                leaf = node.graft(start_index, end_index)
                return node, leaf
            node=next
    if i > 0:
        node.break_node(node.start_index + i)
        node = node.parent
    leaf = node.graft(start_index, end_index)
    return node, leaf


def terminate(text):
    dict = set()
    for char in text[:-1]:
        dict.add(char)
    if text[-1] in dict:
        for i in range(128, 255):
            if not chr(i) in dict:
                text = text + str(chr(i))
                return text
        raise Exception("All ASCII characters are in use in given text. Cannot find terminator.")
    return text


class SuffixTree:
    def __init__(self, text):
        text = terminate(text)
        self.root = Node(text)
        self.name = "SuffixTree with simple initialization"
        self.root.graft(0, len(text))
        for i in range(1, len(text)):
            slowfind(self.root, i, len(text))
    def __str__(self):
        return str(self.root)
    def find(self, label):
        return self.root.find(label)
