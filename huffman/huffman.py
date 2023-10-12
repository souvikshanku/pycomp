from collections import defaultdict
import os

from node import Node


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
    header = str(len(string)) + "\n"

    root_node = _build_tree(string)
    encoding = _get_encoding(root_node)

    for char in set(string):
        header += char + " " + encoding[char] + chr(27)  # Escape

    header += chr(8)  # Backspace

    data = ""
    for char in string:
        data += encoding[char]

    num_extra_0s = ((len(data) // 8) + 1) * 8 - len(data)
    data += "0" * num_extra_0s

    data_bytes = bytearray()
    for i in range(0, len(data), 8):
        data_bytes.append(int(data[i:i + 8], 2))

    return bytearray(header.encode('ascii')) + data_bytes


def compress(path: str):
    with open(path, "rb") as file:
        data = file.read().decode("ascii")

    comp_data = encode(data)

    with open("./compressed.bin", "wb") as file:
        file.write(comp_data)

    og = os.path.getsize(path)
    new = os.path.getsize("./compressed.bin")
    print("Compression Ratio Achieved:", og / new)
    return


def decompress(path: str):
    with open(path, "rb") as file:
        c_data = file.read()

    length = ""

    for i in range(len(c_data)):
        if c_data[i] == 10:  # Space
            break
        length += chr(c_data[i])

    length = int(length)

    header = ""
    for j, byte in enumerate(c_data[i + 1:], i + 1):
        if byte == 8:
            break
        header += chr(byte)

    encoding = {}
    for line in header.split(chr(27))[:-1]:
        encoding[line[2:]] = line[0]

    binary_str = ""

    for k in c_data[j + 1:]:
        binary_str += "0" * (8 - len(bin(k)[2:])) + bin(k)[2:]

    key = ""
    decomp_data = ""

    for char in binary_str:
        if len(decomp_data) < length:
            key += char

            if key in encoding:
                decomp_data += encoding[key]
                key = ""

    with open("./decompressed.txt", "wb") as file:
        file.write(decomp_data.encode("ascii"))

    return


if __name__ == "__main__":
    # from node import tprint
    # string = "aaaaaaaaasavemeeeeee"
    # root_node = _build_tree(string)
    # tprint(root_node)
    # print(_get_encoding(root_node))
    # print(list(encode(string)))

    compress("./sample.txt")
    decompress("./compressed.bin")

    with open("./sample.txt", "rb") as file:
        og = file.read().decode("ascii")

    with open("./decompressed.txt", "rb") as file:
        new = file.read().decode("ascii")

    assert og == new
