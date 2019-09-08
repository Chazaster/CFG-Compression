# Chase Watson
import queue
from LL import LinkedList
from collections import defaultdict

class Repair:
    def __init__(self):
        self.LL = LinkedList()
        self.hash = defaultdict(list)
        self.q = queue.PriorityQueue()

    # Use list comprehension to access values and build LL
    # For now, i will be used as size variable; add size component to LL class later
    def _buildLL(self, string):
        for i in range (len(string)):
            self.LL.append(string[i])
        return self.LL

    # Go through LL and add each pair to the hash table (python dictionary)
    def _buildPairs(self, LL):
        current = LL.start()
        next = LL._next(current)
        hashArray = []

        for i in range(len(LL) - 1):
            # Must convert to string first since current and next are nodes
            tempPair = str(current) + str(next)
            # This gets rid of mysterious backslashes within the concatenated string
            pair = tempPair[1:2] + tempPair[4:5]
            # Get ASCII of pair (as defined in spec) then use built-in hash function to get hash value of each pair
            hashValue = (ord(pair[0]) * 2) + ord(pair[1])
            hashArray.append(hashValue)
            # Add pair to the hash table
            self.hash[hashValue].append(pair)
            # Update current and next nodes to reflect next pair about to be hashed
            current = next
            next = LL._next(current)

        return self.hash, hashArray

    # Used only when populating the hash table
    # Deletes all entries that have <= 1 occurrences of the pair
    def _deleteEntry(self, hash, hashArray):
        originalSize = len(hashArray)
        trimmedHashArray = list(set(hashArray))
        newSize = len(trimmedHashArray)
        # If all entries occur <= 1 time, keep all pairs and add to queue in alpha order
        if (originalSize == newSize):
            # @TODO - alpha order refactor here
            return hash, trimmedHashArray
        # There is a pair that has occurred > 1 time
        else:
            i = 0
            while i < newSize:
                pair = hash[trimmedHashArray[i]]
                if (len(pair) <= 1):
                    del hash[trimmedHashArray[i]]
                    trimmedHashArray.remove(trimmedHashArray[i])
                    newSize -= 1
                else:
                    i += 1
        return hash, trimmedHashArray

    # Now find the pairs that occur >= √n times and place in priority queue
    def _populateQueue(self, hash, n, hashArray):
        #q = queue.PriorityQueue()
        size = 0
        for i in range (len(hashArray)):
            hashEntry = hash[hashArray[i]]
            # @TODO - refactor this, what is n?
            if (len(hashEntry) >= n and len(hashEntry) != 1):
                self.q.put(hashEntry)
            # Gets the number of times a pair has been seen the most in the hash table
            # This is sent to the buildRule function for further implementation
            if (len(hashEntry) > size):
                size = len(hashEntry)
        return self.q, size

    def _getPair(self, hash, queue, hashArray, size):
        # If the queue is empty, go through the hash table finding the first pair without a non terminal
        hashArray.sort()
        if queue.qsize() == 0:
            for i in range(len(hashArray)):
                item = hash[hashArray[i]]
                if (len(item) == size):
                    pair = item[0]
                    return pair
        # If the queue is populated, then take the first item in the priority queue
        else:
            item = queue.get()
            pair = item[0]
            return pair

