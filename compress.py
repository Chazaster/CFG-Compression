# Chase Watson, Adam May, Matt Mulkeen
import queue as queue

def substring(string):
  if len(string) < 4:
    return ""
  for i in range(len(string)-1):
    temp = string[i] + string[i+1]
    if string[i+2:].find(temp) != -1:
      return temp
  return ""

def rule_utility(s, rules):
    arr = []
    for i in range( len(rules) ):
        count = 0
        for j in range( len(s) ):
            if s[j] == rules[i][0]:
                count += 1
        for rl in rules:
            for k in range( len(rl[1]) ):
                if rl[1][k] == rules[i][0]:
                    count += 1
        if count < 2:
            arr.append(i)

    for i in range( len(arr) ):
        char = rules[arr[i]][0]
        pair = rules[arr[i]][1]
        s.replace(pair, char)
        for n in range( len(rules) ):
            rules[n][1] = rules[n][1].replace(char, pair)
        rules = rules[:arr[i]] + rules[arr[i]+1:]
        for j in range( len(arr[i:]) ):
            arr[j + i] -= 1

    return s, rules

def seq(s, string, nonTerminals, rules):
    if string == "" and done(s):
        s, rules = rule_utility(s, rules)
        return s, rules

    if len(string) > 0:
        s += string[0]
        string = string[1:]

    pair = substring(s) #largest_substring_algo1(s)

    if pair == "":
        for rule, thing in rules:
            if s.find(thing) != -1:
                pair = thing
                s = s.replace(pair, rule)
                return seq(s, string, nonTerminals, rules)

    elif len(pair) is not 0:
        s = s.replace(pair, nonTerminals[0])
        rules.append([nonTerminals[0], pair])
        nonTerminals.pop(0)
        return seq(s, string, nonTerminals, rules)


    return seq(s, string, nonTerminals, rules)

def tmpArray(pairArray):
    print("GOT TO TMPARRAY")
    print(pairArray)
    pairArray.pop(0)
    return pairArray

def done(string):
    pair = substring(string)
    if len(pair) is not 0:
        return False
    return True

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

def repair(pairs, queue):
    return input

def main():
    nonTerminals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nonTerms = []
    for i in range(len(nonTerminals)):
        nonTerms.append(nonTerminals[i])
    str = input("Enter a single string of any length using lowercase characters in the language {a - z}: ")
    pairs = createPairs(str)
    rules = []
    S, rules = seq("", str, nonTerms, rules)

    print()
    print("Sequitur Compression:")
    print("S ->", S)
    for rule in rules:
        print(rule[0] + " -> " + rule[1])
main()