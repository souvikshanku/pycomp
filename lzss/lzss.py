import os

BUFFER_SIZE = 256


def _search(SEARCH_BUFFER: str, data, pos) -> tuple[int, int]:
    found_at = -1
    i = 1  # == number of consecutive char matches

    while i <= len(data) - pos and data[pos:pos+i] in SEARCH_BUFFER:
        found_at = SEARCH_BUFFER.find(data[pos:pos+i])
        i += 1

    return found_at, i - 1


def _break(c_data: bytes, comma_pos: int) -> tuple[int, int]:
    # Find the comma
    while True:
        if c_data[comma_pos] == ord(","):
            break
        comma_pos += 1

    # Find the Escape character
    end = comma_pos
    while True:
        if c_data[end] == 27:
            break
        end += 1

    return comma_pos, end


def encode(string: str) -> str:
    SEARCH_BUFFER = ""

    pos = 0
    data = ""

    while pos < len(string):
        found_at, num_matches = _search(SEARCH_BUFFER, string, pos)

        if found_at != -1:
            to_replace_with = (
                chr(27) + str(found_at) + "," + str(num_matches) + chr(27)
            )

            if len(to_replace_with) < num_matches:
                data += to_replace_with
            else:
                data += SEARCH_BUFFER[found_at:found_at + num_matches]
        else:
            data += string[pos]

        if num_matches > 0:
            pos = pos + num_matches
        else:
            pos += 1

        SEARCH_BUFFER = string[:pos][-BUFFER_SIZE:]

    return data


def compress(path: str) -> None:
    with open(path, "rb") as file:
        data = file.read().decode("ascii")

    comp_data = encode(data).encode("ascii")

    with open("./compressed.bin", "wb") as file:
        file.write(comp_data)

    og = os.path.getsize(path)
    new = os.path.getsize("./compressed.bin")
    print("Compression Ratio Achieved:", og / new)
    return


def decompress(path: str) -> None:
    with open(path, "rb") as file:
        c_data = file.read()

    decomp_data = ""

    i = 0
    while i < len(c_data):

        if c_data[i] != 27:
            decomp_data += chr(c_data[i])
            i += 1
        else:
            comma_pos, end = _break(c_data, i)

            start = int(c_data[i + 1:comma_pos])
            num_matches = int(c_data[comma_pos + 1:end])

            search_buffer = [byte for byte in decomp_data[-BUFFER_SIZE:]]
            match = search_buffer[start:start + num_matches]
            decomp_data += "".join(match)

            i = end + 1

    with open("./decompressed.txt", "wb") as file:
        file.write(decomp_data.encode("ascii"))

    return


if __name__ == "__main__":
    compress("sample.txt")
    decompress("compressed.bin")

    with open("./sample.txt", "rb") as file:
        og = file.read().decode("ascii")

    with open("./decompressed.txt", "rb") as file:
        new = file.read().decode("ascii")

    assert og == new
