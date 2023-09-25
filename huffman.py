from collections import defaultdict

from node import Node, tprint


string = "aaaaabbbbc"
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

tprint(list(count.keys())[0])
