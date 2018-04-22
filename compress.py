# Chase Watson, Adam May, Matt Mulkeen
import queue as queue

def createPairs(string):
    pairArray = []
    for i in range (len(string) - 1):
        pairArray.append(string[i] + string[i + 1])
    return pairArray

def pairFrequency(pairs):
    tempArray = []
    q = queue.Queue
    for i in range (len(pairs)):
        size = len(tempArray)
        if size != 0:
            total = 0
            for k in range(size):
                total += tempArray[k]
            q.put(total)
            del tempArray[:]

        temp = pairs[i]
        for j in range (len(pairs)):
            count = 0
            if temp == pairs[j]:
                count += 1
            tempArray.append(count)
    return q

def sequitur(input):
    return input

# Very recursive
def repair(input):
    return input

def main():
    string = input("Enter a single string of any length using lowercase characters in the language {a - z}: ")
    seq = sequitur(string)
    re = repair(string)
    print("After Sequitur: " + seq)
    print("After Re-Pair: " + re)
    pairs = createPairs(string)
    print(pairFrequency(pairs))
main()