# Chase Watson
import math
import time

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

# Counts the # of symbols on the right hand sides of the remaining grammar rules
def sForSequitur(rules):
    s = 0
    temp = [rule[1] for rule in rules]
    for i in range (len(temp)):
        s += len(temp[i])
    return s

def main():
    nonTerminals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nonTerms = [term for term in nonTerminals]
    terminals = "abcdefghijklmnopqrstuvwxyz"
    #terms = [term for term in terminals]
    str = input("Enter a single string of any length using lowercase characters in the language {a - z}: ")
    rules = []
    # Huffman Encoding variables:
    # Variable for total number of rules
    r = 1
    # Variable for sum of right hand sides
    s = 0
    # Variable for # of unique symbols in str
    #a = symbolUniqueness(str, terms)

    start = time.time()
    # Start building grammar rules using Sequitur
    S, rules = seq("", str, nonTerms, rules)
    print()
    print("Sequitur Compression:")
    print("Compressed ->", S)

    # All functions and variable definitions for Huffman Encoding
    for rule in rules:
        print(rule[0] + " -> " + rule[1])
        r += 1
    for i in S:
        s += 1
    s += sForSequitur(rules)
    end = time.time()
    print("Sequitur Runtime:", (end - start))
main()