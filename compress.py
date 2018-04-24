# Chase Watson, Adam May, Matt Mulkeen
''''
Questions:
    1. Are the replace functions for sequitur and repair the same
    or does repair have a different replace function than sequitur?

    2. How do you implement the Linked List, Hash Table, and Priority
    Queue for the Repair replace function as described in the slides?

    3. What is the runtime for sequitur and re-pair?
        O(√n)

    4. How would you Zero-order compress (Huffman Encoding)
    the string after finding all pairs for Re-pair?
'''

import queue

# Function to create pairs from the inputted string
def createPairs(string):
    pairArray = []
    for i in range (len(string) - 1):
        pairArray.append(string[i] + string[i + 1])
    return pairArray

# Function that finds the number of times each pair occurs in the pairArray
def pairFrequency(pairs):
    # tempArray will append a 1 each time a similar pair is seen,
    # and will store a 0 if the pair hasn't been seen yet.
    # This array will get reset each iteration through the loop
    tempArray = []
    # Queue will contain the frequencies and its indicies will correspond to the pairArray indicies
    # This will be linked later in another function
    q = queue.Queue()
    pairsSize = len(pairs)
    for i in range (pairsSize):
        temp = pairs[i]
        # While looping through pairArray, save current pair in temp
        # and loop through pairArray again to compare temp with other
        # elements in the pairArray.
        for j in range(pairsSize):
            count = 0
            # If we see a similar pair, count = 1 and append it to temp array
            if temp == pairs[j]:
                count += 1
            # Otherwise append a 0 (meaning we didnt see the same pair)
            tempArray.append(count)

        # Now we add up the total number of times we saw the pair
        # by just totalling all the 1's in tempArray
        size = len(tempArray)
        # Make sure tempArray is populated, if it isn't don't do anything
        if size != 0:
            total = 0
            for k in range(size):
                total += tempArray[k]
            q.put(total)
            del tempArray[:]
    return q

def sequitur(input):
    return input

def repair(pairs, queue):
    return input

def main():
    string = input("Enter a single string of any length using lowercase characters in the language {a - z}: ")
    seq = sequitur(string)
    print("After Sequitur: " + seq)
    pairs = createPairs(string)
    queue = pairFrequency(pairs)
    #re = repair(pairs, queue)
    #print("After Re-Pair: " + re)
main()