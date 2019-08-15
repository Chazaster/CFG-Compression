##################################
# FUNCTIONS FOR HUFFMAN ENCODING #
##################################

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

# Builds list of unique symbols used on the right hand side of the rules
# Only works for Sequitur but calls symbolTable actually build the list
def buildTableSequitur(S, rules):
    temp = []
    for symbol in S:
        temp.append(symbol)

    rightSideRules = [rule[1] for rule in rules]
    for rule in rightSideRules:
        for symbol in rule:
            temp.append(symbol)

    table = symbolTable(temp)
    return table

# Builds list of unique symbols used on the right hand side of the rules
# Only works for Re-Pair but calls symbolTable actually build the list
def buildTableRepair(S, rules):
    temp = []
    for symbol in S:
        temp.append(symbol)

    for rule in rules:
        for symbol in rule:
            temp.append(symbol)

    table = symbolTable(temp)
    return table

# Does the bulk of work for the sequitur and repair symbol tables
def symbolTable(temp):
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

# Links a binary string to each unique symbol in the symbolTable
# Alphabetically sortted from lowercase to uppercase
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

# Does the dirty work for Huffman Encoding
# Builds the binary string by sequentially looking
# at the symbols on the right side of the rules
def huffmanEncoding(linker, gcSize, S, rules, flag):
    gc = ""
    temp = []
    size = len(linker)
    endMarker = linker[size - 1]

    for i in range (len(S)):
        for tuple in linker:
            if tuple[0] == S[i]:
                gc += tuple[1] + " "

    gc += endMarker[1] + " "

    if (flag == False):
        rightSideRules = [rule[1] for rule in rules]
    else:
        rightSideRules = rules

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

#MAIN#
# Huffman Encoding function calls
            #gcSize, log = grammarCodeSize(s, r, a)
            #symbolTable = buildTableRepair(str, temp)
            #linker = huffmanEncodingHelper(symbolTable, log)
            #grammarCode = huffmanEncoding(linker, gcSize, str, temp, flag)

            #print()
            #print("Encoded Grammar: " + grammarCode)
            #print()
            #print("Key: ")
            #for term in linker:
                #print(term)