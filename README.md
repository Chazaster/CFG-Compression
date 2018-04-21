# CFG Compression Algorithms
In order to compress a Context Free Grammar, the algorithms Sequitur and Re-Pair will be implemented on each CFG to replace repeating non-terminals with new rules.

- Sequitur: You begin with a single S rule and read in each character of the string while adding that character to the S rule. While adding new characters to the S rule, if any repetitions are found in the S rule, we add a new rule displaying the repetitive string, and replace the repetitive parts in the S rule with the nonterminal of the new rule. We repeat this process until we have read the entire string. Rules that are not used in the S rule are removed and added back to any sub rules using them.

- Re-Pair: This method takes in a string input and repeatedly scans it checking for the highest frequency pairs. Once a pair is found, it adds a new rule for this pair and replaces the occurences of these pairs in the S rule. 

