# Chase Watson, Adam May, Matt Mulkeen

def sequitur(input):
    return input

def repair(input):
    return input

def main():
    string = input("Enter a single string of any length using lowercase characters in the language {a - z}")
    choice = int(input("Enter 1 for Sequitur and 2 for Re-Pair"))

    if (choice == 1):
        sequitur(string)

    elif (choice == 2):
        repair(string)

    else:
        print("Invalid Number")

    main()