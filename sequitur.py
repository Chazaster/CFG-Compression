# Chase Watson
#class Sequitur:
#def __init__(self):
import time

def _seq(finalString, string, nonTerminals, rules):
    # @TODO - move this function call to main
    if (string == '' and _done(finalString)):
        rules = _diagramUniqueness1(rules)
        rules = _diagramUniqueness2(rules, nonTerminals)
        s, rules = _rule_utility(finalString, rules)
        return finalString, rules

    if (len(string) > 0):
        finalString += string[0]
        string = string[1:]

    # @TODO - move this function call to main
    pair = _substring(finalString)
    if (pair == ''):
        for rule, thing in rules:
            if (finalString.find(thing) != -1):
                pair = thing
                finalString = finalString.replace(pair, rule)
                return _seq(finalString, string, nonTerminals, rules)

    elif (len(pair) is not 0):
        finalString = finalString.replace(pair, nonTerminals[0])
        rules.append([nonTerminals[0], pair])
        nonTerminals.pop(0)
        return _seq(finalString, string, nonTerminals, rules)
    return _seq(finalString, string, nonTerminals, rules)

def _substring(string):
    #@TODO - Is this because we need 4 chars before we start looking for pairs?
    if (len(string) < 4):
        return ''
    else:
        for i in range(len(string) - 1):
            temp = string[i] + string[i + 1]
            # Returns -1 if there are no pairs, 0 (or something else?) if there are pairs
            if (string[i + 2:].find(temp) != -1):
                return temp
            else:
                return ''
    print("WHY ARE WE HERE")

# Reduction Rule 1
def _rule_utility(s, rules):
    arr = []
    for i in range( len(rules) ):
        count = 0
        for j in range( len(s) ):
            if (s[j] == rules[i][0]):
                count += 1
        for rl in rules:
            for k in range( len(rl[1]) ):
                if (rl[1][k] == rules[i][0]):
                    count += 1
        if (count < 2):
            arr.append(i)

    for i in range( len(arr) ):
        char = rules[arr[i]][0]
        pair = rules[arr[i]][1]
        s.replace(pair, char)
        for n in range( len(rules) ):
            rules[n][1] = rules[n][1].replace(char, pair)
        rules = rules[:arr[i]] + rules[arr[i] + 1:]
        for j in range( len(arr[i:]) ):
            arr[j + i] -= 1
    return s, rules

def _diagramUniqueness1(rules):
    for i in range( len(rules) ):
        for j in range( len(rules) ):
            if (i == j):
                pass
            elif (rules[i][1].find(rules[j][1]) != -1):
                substr = rules[j][1]
                nonterminal = rules[j][0]
                rules[i][1] = rules[i][1].replace(substr, nonterminal)
    return rules

def _diagramUniqueness2(rules, nonTerminals):
    for i in range( len(rules) ):
        for j in range( len(rules) ):
            if (i == j):
                pass
            else:
                # Check for pairs in current 2 rules
                for k in range( len(rules[j][1]) - 1):
                    if k >= len(rules[j][1]) - 1:
                        break
                    pair = rules[j][1][k] + rules[j][1][k + 1]
                    if (rules[i][1].find(pair) != -1):
                        rules[i][1] = rules[i][1].replace(pair, nonTerminals[0])
                        rules[j][1] = rules[j][1].replace(pair, nonTerminals[0])
                        k -= 1
                        nonTerminals.pop(0)
    return rules

    #def _tmpArray(self, pairArray):
    #print(pairArray)
    #pairArray.pop(0)
    #return pairArray

def _done(string):
    # @TODO - move this function call to main
    pair = _substring(string)
    if (len(pair) is not 0):
        return False
    return True

# Counts the # of symbols on the right hand sides of the remaining grammar rules
def _sForSequitur(rules):
    s = 0
    temp = [rule[1] for rule in rules]
    for i in range (len(temp)):
        s += len(temp[i])
    return s

def main():
    str = input("Enter a single string of any length using lowercase characters in the language {a - z}: ")
    originalStr = str
    rules = []
    # Total number of rules, input string is considered a rule
    r = 1
    start = time.time()
    nonTerminals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nonTerms = [term for term in nonTerminals]
    # Sum of right hand sides
    sum = 0
    S, rules = _seq('', str, nonTerms, rules)
    print()
    print("Sequitur Compression:")
    print("Compressed ->", S)

    for rule in rules:
        print(rule[0] + " -> " + rule[1])
        r += 1
    for i in S:
        sum += 1
    sum += _sForSequitur(rules)
    end = time.time()
    print("Sequitur Runtime:", (end - start))

main()