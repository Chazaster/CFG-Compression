# Chase Watson, Adam May, Matt Mulkeen
import queue
import math
from LL import Node
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
# Then have 2 separate functions:
    # Function to handle number of times a pair is seen in the hash table
    # Function to send those remaining pairs to the priority queue
def buildPairs(LL, n, size):
    hash = HashTable()
    current = LL.start()
    next = LL._next(current)
    i = 0
    while (i != LL.__len__() - 1):
        temp = str(current) + str(next)
        # This gets rid of useless and mysterious
        # backslashes within the concatenated string
        pairs = temp[1:2] + temp[4:5]
        hash.add(pairs)
        i += 1
        current = next
        next = LL._next(current)
    return hash

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
        size = len(str)
        LL = buildLL(str)
        n = int(math.sqrt(len(str)))
        hashTable = buildPairs(LL, n, size)
        #queue = pairFrequency(pairs, n)

    else:
        print("Wrong number entered")
main()