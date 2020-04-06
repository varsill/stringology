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

def fastfind(node, start_index, end_index):
    assert node is not None
    l = end_index - start_index
    assert l >= 0
    if l == 0:
        return node, node.start_index
    text = node.text
    node = node.children[text[start_index]]
    while l > node.length():
        start_index += node.length()
        l -= node.length()
        node = node.children[text[start_index]]
    return node, node.start_index + l


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
        text_len = len(text)
        self.root = Node(text)
        self.name = "SuffixTree with McCreight initialization"
        head = self.root
        leaf = self.root.graft(0, text_len)
        for j in range(1, text_len):
            if head == self.root:
                head, leaf = slowfind(self.root, leaf.start_index + 1, leaf.end_index)
                continue
            parent = head.parent
            if parent == self.root:
                head_sl, i = fastfind(parent, head.start_index + 1, head.end_index)
            else:
                head_sl, i = fastfind(parent.suffix_link, head.start_index, head.end_index)
            if i < head_sl.end_index:

                head_sl.break_node(i)
                head_sl = head_sl.parent
                new_head = head_sl
                leaf = new_head.graft(leaf.start_index, leaf.end_index)
            else:
                # s(head) is a node
                new_head, leaf = slowfind(head_sl, leaf.start_index, leaf.end_index)
            head.suffix_link = head_sl
            head = new_head

    def __str__(self):
        return str(self.root)

    def find(self, label):
        return self.root.find(label)