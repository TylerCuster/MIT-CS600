import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

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

# Scoring a word

def get_word_score(word, HAND_SIZE):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    The score for a word is the sum of the points for letters
    in the word, plus 50 points if all n letters are used on
    the first go.

    Letters are scored as in Scrabble; A is worth 1, B is
    worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string (lowercase letters)
    returns: int >= 0
    """
    score = 0
    for letter in word:
        score = score + SCRABBLE_LETTER_VALUES[letter]
    if len(word) == HAND_SIZE:
        score = score + 50
    return score

def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
            print letter,              # print all on the same line
    print                              # print an empty line


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    num_vowels = n / 3
    
    for i in range(num_vowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(num_vowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand


# Update a hand by removing letters

def update_hand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not mutate hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    wordDict = get_frequency_dict(word)
    newhand = hand.copy()
    for letter in wordDict.keys():
        for key in newhand.keys():
            if letter==key:
                newhand[key] = newhand[key]-wordDict[letter]
    return newhand

# Test word validity
def is_valid_word(word, hand, points_dict):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
    
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    """
    newhand = update_hand(hand, word)
    wordDict = get_frequency_dict(word)
    # Check if word contains letter not in hand
    for letter in wordDict.keys():
        if letter not in newhand.keys():
            return False
    # Second, check if word is a real word
    for key in points_dict:
        if word in key and len(word)-len(key)==0:
            # Third, check if word contains more of letter than is in hand
            for letter in newhand.keys():
                if newhand[letter] < 0:
                    return False
            return True
    return False

# Computer picks best word

def pick_best_word(hand, points_dict):
    """
    Return the highest scoring word from points_dict that can be made with
    the given hand.
    
    Return '.' if no words can be made with the given hand.
    """
    current_best_word_score = 0
    exp_hand = hand.copy()
    for key in points_dict.keys():
        if is_valid_word(key, exp_hand, points_dict):
            if points_dict[key] > current_best_word_score:
                current_best_word_score = points_dict[key]
                current_best_word = key
    if current_best_word_score == 0:
        return '.'
    print current_best_word
    return current_best_word

# Permutations function available in 2.6

def permutations(iterable, r=None):
    # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) --> 012 021 102 120 201 210
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = range(n)
    cycles = range(n, n-r, -1)
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return

# Computer picks best word faster

def pick_best_word_faster(hand, rearrange_dict):
    possible_hands = []
    possible_hands_strings = []
    possible_words = []
    n = 0
    print hand
    list_hand = []
    for key in hand:
        if hand[key] != 0:
            list_hand.append(key)
    print list_hand
    for key in hand:
        if hand[key] > 1:
            c1 = 1
            while c1 < hand[key]:
                list_hand.append(key)
                c1 = c1 + 1
    ordered_hand = sorted(list_hand)
    print ordered_hand
    while n < len(ordered_hand):
        n = n + 1
##        print n
        for element in permutations(ordered_hand, n):
            if sorted(element) not in possible_hands:
                possible_hands.append(sorted(element))
    for element in possible_hands:
        possible_hands_strings.append(''.join(element))
##    print possible_hands
##    print possible_hands_strings
    for arrangement in possible_hands_strings:
        for key in rearrange_dict:
            if arrangement == key:
                possible_words.append(rearrange_dict[arrangement])
    print possible_words, "possible words"
    current_best_word_score = 0
    current_best_word = ''
    for word in possible_words:
        if points_dict[word] > current_best_word_score:
            current_best_word_score = points_dict[word]
            current_best_word = word
    print current_best_word
    if current_best_word_score == 0:
        return '.'
    return current_best_word
            
# Playing a hand

def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * When a valid word is entered, it uses up letters from the hand.

    * After every valid word: the score for that word and the total
      score so far are displayed, the remaining letters in the hand 
      are displayed, and the user is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing a single
      period (the string '.') instead of a word.

    * The final score is displayed.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
    """
    import time
    score = 0
    total_time = 0
    k = float(raw_input("Select difficulty level (10 Hard, 1 Easy): "))
    time_limit = get_time_limit(points_dict, k)
    valid = True
    while valid:
        test = True
        second_test = True
        display_hand(hand)
        start = time.time()
        word = pick_best_word_faster(hand, rearrange_dict)
        if word == '.':
            valid = False
            test = False
            second_test = False
            print "End of game."
        end = time.time()
        elapsed = round((end-start),2)
        if elapsed == 0:
            elapsed = 0.1
        print "It took", elapsed, "seconds to provide an answer."
        total_time = total_time + elapsed
        print "You have", time_limit-total_time, "seconds remaining."
        if total_time > time_limit:
            print "Total time exceeds", time_limit, "seconds."
            valid = False
            test = False
            second_test = False
            print "End of game."
        while test:
            if not is_valid_word(word, hand, points_dict):
                print "Invalid word."
                second_test = False
                test = False
            else: test = False
        while second_test:
            hand = update_hand(hand, word)
            score_this_round = get_word_score(word, HAND_SIZE)
            print "Your score this round: ", round((score_this_round/elapsed),2)
            ctr = 0
            score = round((score + score_this_round/elapsed),2)
            second_test = False
            for key in hand.keys():
                    if hand[key] == 0:
                        ctr += 1
                        if ctr == len(hand):
                            print "Out of letters"
                            valid = False
                            break
        print "Total score:", score

# Playing a game

def play_game(word_list):
    """
    Allow the user to play an arbitrary number of hands.

    * Asks the user to input 'n' or 'r' or 'e'.

    * If the user inputs 'n', let the user play a new (random) hand.
      When done playing the hand, ask the 'n' or 'e' question again.

    * If the user inputs 'r', let the user play the last hand again.

    * If the user inputs 'e', exit the game.

    * If the user inputs anything else, ask them again.
    """
    hand = deal_hand(HAND_SIZE) # random init
    test = True
    while test:
        cmd = raw_input('Enter n to deal a new hand, r to replay the last hand, or e to end game: ')
        if cmd == 'n':
            hand = deal_hand(HAND_SIZE)
            play_hand(hand.copy(), word_list)
            print
        elif cmd == 'r':
            play_hand(hand.copy(), word_list)
            print
        elif cmd == 'e':
            break
        else:
            print "Invalid command."

# Time limit for computer player

def get_time_limit(points_dict, k):
    """
    Return the time limit for the computer player as a function of the
    multiplier k.

    points_dict should be the same dictionary that is created by
    get_words_to_points.
    """
    import time
    start_time = time.time()
    for word in points_dict:
        get_frequency_dict(word)
        get_word_score(word, HAND_SIZE)
    end_time = time.time()
    return (end_time - start_time) * k

# Dictionary with all words' scores

def get_words_to_points(word_list):
    wordlist = open(word_list, 'r')
    pdict = {}
    for line in wordlist:
        line = line.lower() #word list is in all caps
        line = line[:-1] #Deletes \n (enter) from line in text doc
        pdict[line] = get_word_score(line, HAND_SIZE) #appends dict with line assigned to score
        if HAND_SIZE < len(line):
            del pdict[line]
    return pdict

# Dictionary with all words sorted

def get_word_rearrangements(points_dict):
    rdict = {}
    for key in points_dict:
        new_string = ""
        for element in sorted(key):
            # creates sorted string for the word
            new_string = new_string + sorted(key)[sorted(key).index(element)]
        rdict[new_string] = key #creates new key in rdict with sorted word with the value the word
    return rdict

#
# Build data structures used for entire session and play game
#

if __name__ == '__main__':
    word_list = load_words()
    points_dict = get_words_to_points('words.txt')
    rearrange_dict = get_word_rearrangements(points_dict)
    play_game('words.txt')
