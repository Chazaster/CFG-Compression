import math
import time
from repair import Repair
#from sequitur import Sequitur

def runRepair(str, originalStr, rules, r):
    start = time.time()
    # Start of printable unicode symbols
    unicodeValStart = int("21", 16)
    originalStrSize = len(str)
    # Start building grammar rules using Re-Pair
    for i in range (originalStrSize):
        # @TODO - refactor so that we don't create a new Repair() object at each iteration
        repair = Repair()
        n = int(math.sqrt(len(str)))
        repair.LL = repair._buildLL(str)
        repair.hash, hashArray = repair._buildPairs(repair.LL)
        repair.hash, hashArray = repair._deleteEntry(repair.hash, hashArray)
        repair.q, size = repair._populateQueue(repair.hash, n, hashArray)

        # If we have reached the end of the input string and there are no more pairs to encode
        if (repair.q.empty() and size <= 1):
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

        pair = repair._getPair(repair.hash, repair.q, hashArray, size)
        unicodeSymbol = chr(unicodeValStart + i)
        rule = unicodeSymbol + " -> " + pair
        rules.append(rule)
        # Replace all pairs in input string with rule, then run re-pair over string with new rule
        str = str.replace(pair, unicodeSymbol)

def runSequitur(str, originalStr, rules, r):
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

def main():
    str = input("Enter a single string of any length using lowercase characters in the language {a - z}: ")
    originalStr = str
    rules = []
    # Total number of rules, input string is considered a rule
    r = 1
    selection = int(input("Type 1 to compress wtih Re-Pair or 2 to compress with Sequitur: "))

    if (selection == 1):
        runRepair(str, originalStr, rules, r)
    elif (selection == 2):
        runSequitur(str, originalStr, rules, r)
    else:
        print("Invalid number, quitting now")
main()