import math
import hashlib

class BloomFilter:
    """
    Bloom Filter Data Structure Implementation.
    """
    
    def __init__(self, expected_items: int, fp_rate: float):
        self.expected_items = expected_items
        self.fp_rate = fp_rate
        
        self.size = self._get_size(expected_items, fp_rate)
        
        self.hash_count = self._get_hash_count(self.size, expected_items)
        
        self.bit_array = [False] * self.size

    def _get_hash_indices(self, item) -> list:
        """
        Creates a family of 'k' hash functions using hashlib.md5.
        Returns a list of 'k' indices for the given item.
        """
        indices = []
        item_str = str(item)
        
        for i in range(self.hash_count):
            seeded_item = f"{item_str}_{i}".encode('utf-8')
            
            hash_val = int(hashlib.md5(seeded_item).hexdigest(), 16)
            index = hash_val % self.size
            indices.append(index)
            
        return indices
        
    def add(self, item):
        """
        Inserts an item into the Bloom Filter by setting the hashed indices to True.
        """
        for index in self._get_hash_indices(item):
            self.bit_array[index] = True

    def check(self, item) -> bool:
        """
        Checks if an item is in the Bloom Filter.
        Returns True if all hashed indices are True (possibly in set).
        Returns False if any hashed index is False (definitely not in set).
        """
        for index in self._get_hash_indices(item):
            if not self.bit_array[index]:
                return False
        return True

    def _get_size(self, n, p) -> int:
        m = -(n * math.log(p)) / (math.log(2)**2)
        return int(m)

    def _get_hash_count(self, m, n) -> int:
        k = (m / n) * math.log(2)
        return int(k)