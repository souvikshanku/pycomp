from collections import defaultdict

from node import Node, tprint


def _build_tree(string: str) -> Node:
    count = defaultdict(int)

    for char in string:
        count[Node(char)] += 1

    count = {key: count[key] for key in sorted(count, key=count.get)}

    for _ in range(len(count) - 1):
        count = {key: count[key] for key in sorted(count, key=count.get)}

        root = Node(list(count.keys())[0].value + list(count.keys())[1].value)
        root.set_children(list(count.keys())[:2])

        count[root] = sum(list(count.values())[:2])
        del count[root.left]
        del count[root.right]

    return list(count.keys())[0]


def _dfs(node: Node, path: str, encoding: dict) -> dict:
    if node.left is not None:
        _dfs(node.left, path + "0", encoding)
    else:
        encoding[node.value] = path

    if node.right is not None:
        _dfs(node.right, path + "1", encoding)
    else:
        encoding[node.value] = path

    return encoding


def _get_encoding(node) -> dict:
    encoding = {}
    path = ""
    encoding = _dfs(node, path, encoding)

    return encoding


def encode(string: str) -> bytearray:
    root_node = _build_tree(string)
    encoding = _get_encoding(root_node)

    header = ""
    for char in set(string):
        header += char + " " + encoding[char] + "\n"

    header += chr(8)

    data = ""
    for char in string:
        data += encoding[char]

    num_extra_0s = ((len(data) // 8) + 1) * 8 - len(data)
    data += "0" * num_extra_0s

    data_bytes = bytearray()
    for i in range(0, len(data), 8):
        data_bytes.append(int(data[i:i + 8], 2))

    return bytearray(header.encode('ascii')) + data_bytes


if __name__ == "__main__":
    string = "aaaaaaaaasavemeeeeee"
    root_node = _build_tree(string)
    tprint(root_node)
    print(_get_encoding(root_node))
    print(list(encode(string)))
