with open("sample.txt", "rb") as file:
    data = file.read().decode("ascii")


print(data)
# print(len(data))

BUFFER_SIZE = 32
SEARCH_BUFFER = ""
final = ""


def search(SEARCH_BUFFER, data, pos):
    found_at = -1

    while True:
        if pos < len(data) and data[pos] in SEARCH_BUFFER:
            found_at = SEARCH_BUFFER.find(data[pos])
            # print(data[pos], "found_at - ", found_at)
            pos += 1
        else:
            return found_at, pos


pos = 0

while pos < len(data):

    # print(f"'{SEARCH_BUFFER}', pos = {pos}")
    found_at, end = search(SEARCH_BUFFER, data, pos)
    # print(f"<{found_at}, {end - pos}>")

    if found_at != -1:
        final += f"<{found_at}, {end - pos}>"
    else:
        final += data[pos]

    if end - pos > 1:
        pos = end
    else:
        pos += 1

    SEARCH_BUFFER = data[:pos][-BUFFER_SIZE:]

    # print(f"'{SEARCH_BUFFER}'", "\n--------")

print(final)
