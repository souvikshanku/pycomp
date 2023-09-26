from collections import defaultdict

from node import Node, tprint


def build_tree(string: str) -> Node:
    count = defaultdict(int)

    for char in string:
        count[Node(char)] += 1

    count = {key: count[key] for key in sorted(count, key=count.get)}

    for i in range(len(count) - 1):
        count = {key: count[key] for key in sorted(count, key=count.get)}

        root = Node(list(count.keys())[0].value + list(count.keys())[1].value)
        root.set_children(list(count.keys())[:2])

        count[root] = sum(list(count.values())[:2])
        del count[root.left]
        del count[root.right]

    return list(count.keys())[0]


def _dfs(node: Node, path: str, encoding: dict):
    if node.left is not None:
        _dfs(node.left, path + "0", encoding)
    else:
        encoding[node.value] = path

    if node.right is not None:
        _dfs(node.right, path + "1", encoding)
    else:
        encoding[node.value] = path

    return encoding


def get_encoding(node) -> dict:
    encoding = {}
    path = ""

    encoding = _dfs(node, path, encoding)

    return encoding


if __name__ == "__main__":
    string = "aaaaaaaaaddbccc"
    node = build_tree(string)
    tprint(node)
    print(get_encoding(node))
