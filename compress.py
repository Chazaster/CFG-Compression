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
    for i in range(LL.__len__() - 1):
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
    # NEEDS TO BE TESTED THOROUGHLY
    # If there is nothing in the queue, go through the hash table
    # finding the first pair without a non terminal
    if queue.empty() and size >= 2:
        priority = False
        hashArray = list(set(hashArray))
        for i in range(len(hashArray)):
            temp = hashArray[i]
            s = hash.get(temp)
            for i in range (len(s)):
                for j in range (len(nonTerms)):
                    if s[i] != nonTerms[j]:
                        priority = True
                    else:
                        priority = False
            if priority == True:
                rule = cleanRule(s)
                return rule
    # If the queue is not empty, then take the first item in the priority queue
    else:
        item = queue.get()
        rule = cleanRule(item)
        return rule

# Pulls out individual pair from passed hash table sublist
def cleanRule(rule):
    clean = ""
    i = 0
    while (i != 1):
        for j in rule[i]:
            clean += j
            i += 1
    return clean

def main():
    num = int(input("Enter 1 for Sequitur or 2 for Re-Pair: "))
    nonTerminals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nonTerms = []
    for i in range(len(nonTerminals)):
        nonTerms.append(nonTerminals[i])
    str = input("Enter a single string of any length using lowercase characters in the language {a - z}: ")
    rules = []

    if (num == 1):
        S, rules = seq("", str, nonTerms, rules)
        print()
        print("Sequitur Compression:")
        print("S ->", S)
        for rule in rules:
            print(rule[0] + " -> " + rule[1])

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
                return str, rules
            pair = getPair(hashTable, q, nonTerms, hashArray, size)
            rule = nonTerms[i] + " -> " + pair
            rules.append(rule)
            str = str.replace(pair, nonTerms[i])

    else:
        print("Wrong number entered")
main()