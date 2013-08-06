import random

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print "  ", len(wordlist), "words loaded."
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq


# (end of helper code)
# -----------------------------------

# Actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program.
wordlist = load_words()

def word_possibility(fragment, word):
    """Checks if word can possibly be formed beginning with letters in fragment"""

    for n in range(0, len(fragment)):
        if len(word) < len(fragment):
            return False
        if word[n] != fragment[n]:
            return False
    return True

def player(turn):
    """ Determines player based on turn """
    if turn%2 == 0:
        return '1'
    else: return '2'
    
def ghost():
    """ Ghost game """
    print "Welcome to Ghost!"
    print
    fragment = []
    turn = 1
    word = ''
    
    while True:
        # counts turn
        turn += 1
        print "Current word fragment:", word
        ctr = 0
        possibility = 0
        if turn > 2 and len(word) > 3:
            # searches word list by line
            for line in wordlist:
                ctr += 1
                # if it finds the current word, previous player loses
                if line == word:
                    print "Player " + player(turn-1) + " loses because " + word + " is a word."
                    print "Player " + player(turn) + " wins!"
                    return None
                # searches through the whole thing and if a word is possible
                # we give possibility the value 1
                if word_possibility(word, line) == True:
                    possibility = 1
        # if it searched through the entire word list and no word was possible, player loses
        if ctr == len(wordlist) and possibility != 1:
            print "Player " + player(turn-1) + " loses because no word begins with " + word
            print "Player " + player(turn) + " wins!"
            return None
        print "Player " + player(turn) + "'s turn"
        # player inputs letter, program checks if it is letter and if so adds it to the fragment
        while True:
            letter = str(raw_input("Player " + player(turn) + " says letter: "))
            letter = letter.lower()
            if letter in string.ascii_letters:
                fragment.append(letter)
                word = word + str(fragment[-1])
                break
            else: print "Not a letter. Enter a letter."
        print
