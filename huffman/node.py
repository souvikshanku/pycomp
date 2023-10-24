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
        tprint(node.right, level + 1)
        print(' ' * 6 * level + '-> ' + str(node.value))
        tprint(node.left, level + 1)


if __name__ == "__main__":
    node1 = Node("1")
    node2 = Node("2")
    node3 = Node("3")
    node4 = Node("4")
    node5 = Node("5")
    node3.set_children([node4, node5])
    node1.set_children([node2, node3])
    tprint(node1)
