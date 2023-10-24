
Implementation of Huffman Code and LZSS compression algorithm.

#### Example Usage
```python
from huffman.huffman import compress, decompress

compress("./sample.txt")
decompress("./compressed.bin")

with open("./sample.txt", "rb") as file:
    og = file.read().decode("ascii")

with open("./decompressed.txt", "rb") as file:
    new = file.read().decode("ascii")

assert og == new
```

#### References
*  [The Hitchhiker’s Guide to Compression](https://go-compression.github.io/)
* [Huffman Coding and Data Compression](https://web.stanford.edu/class/archive/cs/cs106b/cs106b.1214/handouts/290%20Huffman%20Coding.pdf)

#### ToDo
Implement more compression algorithms.
