
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return f"Node({self.value})"

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def set_children(self, children) -> None:
        self.left = children[0]
        self.right = children[1]


def tprint(node, level=0):
    if node is not None and node.value is not None:
        tprint(node.left, level + 1)
        print(' ' * 6 * level + '-> ' + str(node.value))
        tprint(node.right, level + 1)
