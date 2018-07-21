# Chase Watson

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
        else:
            # Collision handling done here
            # Check to see if items already in cell are same as current pair
            for value in self.table[key_hash]:
                # If true, append
                if key_value == value:
                    self.table[key_hash].append(key_value)
                    return True
                # If false, use linear probing to handle collisions
                else:
                    entrySize = 0
                    new_value = []

                    # To prevent out-of-range errors
                    if key_hash == self.size - 1:
                        new_hash = 0
                    else:
                        new_hash = key_hash + 1

                    # Get size of entry in hash table
                    for i in self.table[new_hash]:
                        entrySize += 1
                        new_value = [i[0]]

                    # Check if value within the entry at new_hash is the same as the current key_value
                    if key_value == new_value:
                        self.table[new_hash].append(key_value)
                        return True

                    # If next hash table entry is empty, insert
                    elif entrySize == 0:
                        self.table[new_hash].append(key_value)
                        return True

                    # Otherwise, we continue through hash table until we find a match or empty entry
                    else:
                        while entrySize != 0:
                            entrySize = 0

                            if new_hash == self.size - 1:
                                new_hash = 0
                            else:
                                new_hash += 1

                            for i in self.table[new_hash]:
                                entrySize += 1
                                new_value = [i[0]]

                            if key_value == new_value:
                                self.table[new_hash].append(key_value)
                                return True

                        self.table[new_hash].append(key_value)
                        return True

            self.table[key_hash].append(key_value)
            return True

    def get(self, key):
        current = self.table[key]
        if current is not None:
            # Might not work properly, might change
            return current
        return None

    def delete(self, key, hash):
        if self.table[hash] is None:
            return False
        else:
            # Similar to append, might change if add doesn't work
            self.table[hash].pop()
            return True