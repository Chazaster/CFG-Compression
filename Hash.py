# Chase Watson, Adam May, Matt Mulkeen

class HashTable:
    def __init__(self):
        self.size = 256
        self.table = [[] for _ in range(self.size)]

    # For the hashing function, we get the ASCII value of each
    # character in the pair and mod that with the table size.
    # Since the Hash Table is initialized as a list of lists,
    # similar pairs would be mapped to the same entry in the table
    def _get_hash(self, key):
        hash = 0
        # To prevent 'be' and 'eb' from existing in the same sublist,
        # we grab the ASCII value of the first element in the string
        # and add it to the resulting hash value before it is modded
        temp = ord(key[0])
        for char in str(key):
            hash += ord(char)
        hash += temp
        return hash % self.size

    def add(self, key):
        # Get the index of the entry using the hash function
        key_hash = self._get_hash(key)
        key_value = [key]
        # Check to see if the cell in the table is empty or not
        if self.table[key_hash] is None:
            # Might make list of a list of a list here, might change
            self.table[key_hash] = list([key_value])
            return True
        # Collision handling done here
        else:
            self.table[key_hash].append(key_value)
            return True

    def get(self, key):
        current = self.table[key]
        if current is not None:
            # Might not work properly, might change
            return current
        return None

    def delete(self, key):
        key_hash = self._get_hash(key)
        if self.table[key_hash] is None:
            return False
        else:
            # Similar to append, might change if add doesn't work
            self.table[key_hash].pop(key)
            return True