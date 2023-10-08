with open("sample.txt", "rb") as file:
    data = file.read().decode("ascii")

print(data)

BUFFER_SIZE = 16
SEARCH_BUFFER = ""
final = ""


def search(SEARCH_BUFFER, data, pos):
    found_at = -1
    i = 1  # == number of consecutive char matches

    while i <= len(data) - pos and data[pos:pos+i] in SEARCH_BUFFER:
        found_at = SEARCH_BUFFER.find(data[pos:pos+i])
        # print(data[pos:pos+i], "found_at - ", found_at)
        i += 1

    return found_at, i - 1


pos = 0

while pos < len(data):
    found_at, num_matches = search(SEARCH_BUFFER, data, pos)

    if found_at != -1:
        to_replace_with = f"<{found_at},{num_matches}>"

        if len(to_replace_with) < num_matches:
            final += f"<{found_at},{num_matches}>"
        else:
            final += SEARCH_BUFFER[found_at:found_at + num_matches]
    else:
        final += data[pos]

    if num_matches > 0:
        pos = pos + num_matches
    else:
        pos += 1

    SEARCH_BUFFER = data[:pos][-BUFFER_SIZE:]

print(final)
