class Node:
    def __init__(self, data, next_=None, prev=None):
        self.data = data
        self.next = next_
        self.prev = prev

    def __repr__(self):
        return f"{self.data!r}"

    def __lt__(self, other):
        if isinstance(other, Node):
            return self.data < other.data
        return self.data < other

    def __gt__(self, other):
        if isinstance(other, Node):
            return self.data > other.data
        return self.data > other
