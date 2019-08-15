# Chase Watson
import queue
import math
from LL import LinkedList
from collections import defaultdict
import time

# Use list comprehension to access values and build LL
# For now, i will be used as size variable; add size component to LL class later
def buildLL(string):
    LL = LinkedList()
    for i in range (len(string)):
        LL.append(string[i])
    return LL

# Go through LL and add each pair to the hash table (python dictionary)
def buildPairs(LL):
    hash = defaultdict(list)
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
        hash[hashValue].append(pair)
        # Update current and next nodes to reflect next pair about to be hashed
        current = next
        next = LL._next(current)

    hash, hashArray = deleteEntry(hash, hashArray)
    return hash, hashArray

# Used only when populating the hash table
# Deletes all entries that have <= 1 occurrences of the pair
def deleteEntry(hash, hashArray):
    originalSize = len(hashArray)
    slimmedHashArray = list(set(hashArray))
    newSize = len(slimmedHashArray)
    # If all entries occur <= 1 time, keep all pairs and add to queue in alpha order
    if (originalSize == newSize):
        # @TODO - alpha order refactor here
        return hash, slimmedHashArray
    # There is a pair that has occurred > 1 time
    else:
        i = 0
        while i < newSize:
            pair = hash[slimmedHashArray[i]]
            if (len(pair) <= 1):
                del hash[slimmedHashArray[i]]
                #hash.delete(cleanRule(pair), hashArray[i])
                slimmedHashArray.remove(slimmedHashArray[i])
                newSize -= 1
            else:
                i += 1
    return hash, slimmedHashArray

# Now find the pairs that occur >= √n times and place in priority queue
def populateQueue(hash, n, hashArray):
    q = queue.PriorityQueue()
    size = 0
    for i in range (len(hashArray)):
        hashEntry = hash[hashArray[i]]
        # @TODO - refactor this, what is n?
        if (len(hashEntry) >= n and len(hashEntry) != 1):
            q.put(hashEntry)
        # Gets the number of times a pair has been seen the most in the hash table
        # This is sent to the buildRule function for further implementation
        if (len(hashEntry) > size):
            size = len(hashEntry)
    return q, size

def getPair(hash, queue, hashArray, size):
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

def main():
    str = input("Enter a single string of any length using lowercase characters in the language {a - z}: ")
    originalStr = str
    rules = []
    # Variable for total number of rules, input string is considered a rule
    r = 1
    # Start of printable unicode symbols
    unicodeValStart = int('21', 16)
    start = time.time()
    originalStrSize = len(str)
    # Start building grammar rules using Re-Pair
    for i in range (originalStrSize):
        n = int(math.sqrt(len(str)))
        LL = buildLL(str)
        hashTable, hashArray = buildPairs(LL)
        q, size = populateQueue(hashTable, n, hashArray)

        # If we have reached the end of the input string and there are no more pairs to encode
        if (q.empty() and size <= 1):
            # End timer and finish compression
            end = time.time()

            # Holds all pairs that were encoded
            representedPairs = []
            print("\nRe-Pair Compression:\n")
            print("Original input string:   ", originalStr)
            print("Compressed input string: ", str)
            if (len(rules) != 0):
                for rule in rules:
                    print("  ", rule)
                    r += 1
                for item in rules:
                    representedPairs.append(item[5:])

            compressedStrSize = len(str)
            print("\nRe-Pair Runtime:", (end - start))
            print("Length of original input string: ", originalStrSize)
            print("Length of compressed input string: ", compressedStrSize)
            return str, rules

        pair = getPair(hashTable, q, hashArray, size)
        unicodeSymbol = chr(unicodeValStart + i)
        rule = unicodeSymbol + " -> " + pair
        rules.append(rule)
        # Replace all pairs in input string with rule, then run re-pair over string with new rule
        str = str.replace(pair, unicodeSymbol)
main()