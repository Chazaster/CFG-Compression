# Chase Watson, Adam May, Matt Mulkeen
import queue
import math
from LL import LinkedList
from Hash import HashTable

# FUNCTIONS FOR SEQUITUR
def substring(string):
  if len(string) < 4:
    return ""
  for i in range(len(string)-1):
    temp = string[i] + string[i+1]
    if string[i+2:].find(temp) != -1:
      return temp
  return ""

# Reduction Rule 1
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

def diagramUniqueness1(rules):
  for i in range( len(rules) ):
    for j in range( len(rules) ):
      if i == j:
        pass
      elif rules[i][1].find(rules[j][1]) != -1:
        substr = rules[j][1]
        nonterminal = rules[j][0]
        rules[i][1] = rules[i][1].replace(substr, nonterminal )

  return rules

def diagramUniqueness2(rules, nonTerminals):
  for i in range( len(rules) ):
    for j in range( len(rules) ):
      if i == j:
        pass
      else:
        # Check for pairs in current 2 rules
        for k in range( len(rules[j][1]) -1):
          if k >= len(rules[j][1])-1:
            break
          pair = rules[j][1][k] + rules[j][1][k+1]
          if rules[i][1].find(pair) != -1:
            rules[i][1] = rules[i][1].replace(pair, nonTerminals[0])
            rules[j][1] = rules[j][1].replace(pair, nonTerminals[0])
            k -= 1
            nonTerminals.pop(0)

  return rules

def seq(s, string, nonTerminals, rules):
    if string == "" and done(s):
        rules = diagramUniqueness1(rules)
        rules = diagramUniqueness2(rules, nonTerminals)
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

# FUNCTIONS FOR RE-PAIR

# Use list comprehension to access values and build LL
def buildLL(string):
    LL = LinkedList()
    for i in range (len(string)):
        LL.append(string[i])
    return LL

# Go through LL and add each pair to the hash table
def buildPairs(LL):
    hash = HashTable()
    current = LL.start()
    next = LL._next(current)
    hashArray = []
    for i in range(len(LL) - 1):
        temp = str(current) + str(next)
        # This gets rid of useless and mysterious backslashes within the concatenated string
        pairs = temp[1:2] + temp[4:5]
        # Get the hash value of each pair, store in array, and pass to populateQueue
        hashValue = hash._get_hash(pairs)
        hashArray.append(hashValue)
        # Where we add all pairs to the hash table
        hash.add(pairs)
        current = next
        next = LL._next(current)
    hash, hashArray = deleteEntry(hash, hashArray)
    return hash, hashArray

# Used only when populating the hash table
# Deletes all entries that have <= 1 occurrences of the pair
def deleteEntry(hash, hashArray):
    hashArray = list(set(hashArray))
    size = len(hashArray)
    i = 0
    while i < size:
        temp = hash.get(hashArray[i])
        if (len(temp) <= 1):
            hash.delete(cleanRule(temp))
            hashArray.remove(hashArray[i])
            size -= 1
        else:
            i += 1
    return hash, hashArray

# Now find the pairs that occur >= √n times and place in priority queue
def populateQueue(hash, n, hashArray):
    q = queue.PriorityQueue()
    size = 0
    # Set removes any duplicates from the array, doing this because we
    # get all entries of the same hash from the hash table
    hashArray = list(set(hashArray))
    for i in range (len(hashArray)):
        temp = hashArray[i]
        s = hash.get(temp)
        if (len(s) >= n and len(s) != 1):
            q.put(s)
        # Gets the number of times a pair has been seen the most in the hash table
        # This is sent to the buildRule function for further implementation
        if (len(s) > size):
            size = len(s)
    return q, size

def getPair(hash, queue, nonTerms, hashArray, size):
    # If there is nothing in the queue, go through the hash table
    # finding the first pair without a non terminal
    #priority = False
    hashArray.sort()
    if queue.empty():
        for i in range(len(hashArray)):
            temp = hashArray[i]
            s = hash.get(temp)
            if (len(s) == size):
                rule = cleanRule(s)
                return rule
    # If the queue is not empty, then take the first item in the priority queue
    else:
        item = queue.get()
        rule = cleanRule(item)
        return rule

# Pulls out individual pair from passed hash table sublist
# Removes gunk like comet on a toilet
def cleanRule(rule):
    clean = ""
    i = 0
    while (i != 1):
        for j in rule[i]:
            clean += j
            i += 1
    return clean

# FUNCTIONS FOR HUFFMAN ENCODING

# Counts the # of unique symbols in input string, used for a in encoding process
def symbolUniqueness(str, terms):
    a = 0
    for i in str:
        for j in range (len(terms)):
            if i == terms[j]:
                a += 1
                del terms[j]
                break
            else:
                continue
    return a

# s = sum of # of symbols on right hand side of all rules
# r = total # of rules
# a = # of unique symbols in input string
def grammarCodeSize(s, r, a):
    # log2 calculates the log base 2 of r + a and is used
    # to determine the size of each symbol's bit string
    x = r + a
    log2 = math.log(x, 2.0)
    log = math.ceil(log2)
    # temp stores the result of s + r - 1, used for size of gc
    temp = s + r - 1
    gcSize = temp * log
    return gcSize, log

# Counts the # of symbols on the right hand sides of the remaining grammar rules
def sForSequitur(rules):
    s = 0
    temp = [rule[1] for rule in rules]
    for i in range (len(temp)):
        s += len(temp[i])
    return s

def buildTable(S, rules):
    temp = []
    for symbol in S:
        temp.append(symbol)

    rightSideRules = [rule[1] for rule in rules]
    for rule in rightSideRules:
        for symbol in rule:
            temp.append(symbol)

    cleanedTemp = list(set(temp))
    lower = []
    upper = []
    for i in cleanedTemp:
        if i.islower():
            lower.append(i)
        else:
            upper.append(i)
    lower.sort()
    upper.sort()
    symbolTable = lower + upper
    return symbolTable

def huffmanEncodingHelper(symbolTable, log):
    count = 0
    linker = []
    padding = "{0:0" + str(log) + "b}"
    for i in range(len(symbolTable)):
        temp = [symbolTable[i], padding.format(i)]
        linker.append(temp)
        count += 1
    linker.append(['#', padding.format(count)])
    return linker

def huffmanEncoding(linker, gcSize, S, rules):
    gc = ""
    temp = []
    size = len(linker)
    endMarker = linker[size - 1]
    for i in range (len(S)):
        for tuple in linker:
            if tuple[0] == S[i]:
                gc += tuple[1] + " "

    gc += endMarker[1] + " "

    rightSideRules = [rule[1] for rule in rules]
    for rule in rightSideRules:
        for symbol in rule:
            temp.append(symbol)
        temp.append(endMarker[1])
    del temp[len(temp) - 1]

    for i in range (len(temp)):
        symbol = temp[i]
        for tuple in linker:
            if tuple[0] == symbol:
                gc += tuple[1] + " "
            elif symbol == endMarker[1]:
                gc += endMarker[1] + " "
                break

    return gc

def main():
    num = int(input("Enter 1 for Sequitur or 2 for Re-Pair: "))
    nonTerminals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nonTerms = [term for term in nonTerminals]
    terminals = "abcdefghijklmnopqrstuvwxyz"
    terms = [term for term in terminals]
    str = input("Enter a single string of any length using lowercase characters in the language {a - z}: ")
    rules = []
    # Variable for total number of rules
    r = 1
    # Variable for sum of right hand sides
    s = 0
    # Variable for # of unique symbols in str
    a = symbolUniqueness(str, terms)

    if (num == 1):
        S, rules = seq("", str, nonTerms, rules)
        print()
        print("Sequitur Compression:")
        print("S ->", S)
        for rule in rules:
            print(rule[0] + " -> " + rule[1])
            r += 1
        for i in S:
            s += 1
        s += sForSequitur(rules)
        gcSize, log = grammarCodeSize(s, r, a)
        symbolTable = buildTable(S, rules)
        linker = huffmanEncodingHelper(symbolTable, log)
        grammarCode = huffmanEncoding(linker, gcSize, S, rules)
        print()
        print("Encoded Grammar: " + grammarCode)
        return str, rules, grammarCode

    elif (num == 2):
        for i in range (len(str)):
            n = int(math.sqrt(len(str)))
            LL = buildLL(str)
            hashTable, hashArray = buildPairs(LL)
            q, size = populateQueue(hashTable, n, hashArray)
            if (q.empty() and size <= 1):
                print()
                print("Re-Pair Compression:")
                print("S ->", str)
                for rule in rules:
                    print(rule)
                    r += 1
                return str, rules
            pair = getPair(hashTable, q, nonTerms, hashArray, size)
            rule = nonTerms[i] + " -> " + pair
            rules.append(rule)
            str = str.replace(pair, nonTerms[i])

    else:
        print("Wrong number entered")
main()