import hashlib
import time

class Block:
    def __init__(self, index, data, previous_hash):
        self.index=index
        self.timestamp=time.time()
        self.data =data
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()
    def compute_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()


gensis_block = Block(0,"Genesis Block","0")
print(f"Genesis Block Hash:{gensis_block.hash}")
