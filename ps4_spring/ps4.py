# 6.00 Problem Set 4
#
# Caesar Cipher Skeleton
#
import string
import random

WORDLIST_FILENAME = "words.txt"

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print "  ", len(wordlist), "words loaded."
    return wordlist

wordlist = load_words()

def is_word(wordlist, word):
    """
    Determines if word is a valid word.

    wordlist: list of words in the dictionary.
    word: a possible word.
    returns True if word is in wordlist.

    Example:
    >>> is_word(wordlist, 'bat') returns
    True
    >>> is_word(wordlist, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in wordlist

def random_word(wordlist):
    """
    Returns a random word.

    wordlist: list of words  
    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

def random_string(wordlist, n):
    """
    Returns a string containing n random words from wordlist

    wordlist: list of words
    returns: a string of random words separated by spaces.
    """
    return " ".join([random_word(wordlist) for _ in range(n)])

def random_scrambled(wordlist, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    wordlist: list of words
    n: number of random words to generate and scamble
    returns: a scrambled string of n random words


    NOTE:
    This function will ONLY work once you have completed your
    implementation of apply_shifts!
    """
    s = random_string(wordlist, n) + " "
    shifts = [(i, random.randint(0, 26)) for i in range(len(s)) if s[i-1] == ' ']
    return apply_shifts(s, shifts)[:-1]

def get_fable_string():
    """
    Returns a fable in encrypted text.
    """
    f = open("fable2.txt", "r")
    fable = str(f.read())
    f.close()
    return fable


# (end of helper code)
# -----------------------------------

#
# Problem 1: Encryption
#
def build_coder(shift):
    """
    Returns a dict that can apply a Caesar cipher to a letter.
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: -27 < int < 27
    returns: dict

    Example:
    >>> build_coder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)
    """
    ### TODO.
    shifted_dictionary = {}
    Shifted_dictionary = {}
    Letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
               'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
               'X', 'Y', 'Z', ' ']
    letters = [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
               'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
               'u', 'v', 'w', 'x', 'y', 'z']
    for i in range(len(letters)):
        if i + shift > len(letters)-2:
            shifted_dictionary[letters[i]] = letters[shift-1-(len(letters)-1-letters.index(letters[i]))]
        else:
            shifted_dictionary[letters[i]] = letters[i+shift]
    for i in range(len(Letters)):
        if i + shift > len(Letters)-2:
            Shifted_dictionary[Letters[i]] = Letters[shift-1-(len(Letters)-1-Letters.index(Letters[i]))]
        else:
            Shifted_dictionary[Letters[i]] = Letters[i+shift]
    Shifted_dictionary.update(shifted_dictionary)
    return Shifted_dictionary

def build_encoder(shift):
    """
    Returns a dict that can be used to encode a plain text. For example, you
    could encrypt the plain text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_encoder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    ### TODO.
    return build_coder(shift)


def build_decoder(shift):
    """
    Returns a dict that can be used to decode an encrypted text. For example, you
    could decrypt an encrypted text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    >>>decrypted_text = apply_coder(plain_text, decoder)
    
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict
    Example:
    >>> build_decoder(3)
    {' ': 'x', 'A': 'Y', 'C': ' ', 'B': 'Z', 'E': 'B', 'D': 'A', 'G': 'D',
    'F': 'C', 'I': 'F', 'H': 'E', 'K': 'H', 'J': 'G', 'M': 'J', 'L': 'I',
    'O': 'L', 'N': 'K', 'Q': 'N', 'P': 'M', 'S': 'P', 'R': 'O', 'U': 'R',
    'T': 'Q', 'W': 'T', 'V': 'S', 'Y': 'V', 'X': 'U', 'Z': 'W', 'a': 'y',
    'c': ' ', 'b': 'z', 'e': 'b', 'd': 'a', 'g': 'd', 'f': 'c', 'i': 'f',
    'h': 'e', 'k': 'h', 'j': 'g', 'm': 'j', 'l': 'i', 'o': 'l', 'n': 'k',
    'q': 'n', 'p': 'm', 's': 'p', 'r': 'o', 'u': 'r', 't': 'q', 'w': 't',
    'v': 's', 'y': 'v', 'x': 'u', 'z': 'w'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    ### TODO.
    return build_coder(-shift)

def apply_coder(text, coder):
    """
    Applies the coder to the text. Returns the encoded text.

    text: string
    coder: dict with mappings of characters to shifted characters
    returns: text after mapping coder chars to original text

    Example:
    >>> apply_coder("Hello, world!", build_encoder(3))
    'Khoor,czruog!'
    >>> apply_coder("Khoor,czruog!", build_decoder(3))
    'Hello, world!'
    """
    ### TODO.
    shifted_dictionary = coder
    code_list = []
    code_word = ""
    for char in text:
        char_ = 0
        for key in shifted_dictionary:
            if key == char:
                char_ = 1
        if char_ == 1:
            code_list.append(shifted_dictionary[char])
        else:
            code_list.append(char)
    for i in range(len(code_list)):
        code_word = code_word + code_list[i]
    return code_word
  

def apply_shift(text, shift):
    """
    Given a text, returns a new text Caesar shifted by the given shift
    offset. The empty space counts as the 27th letter of the alphabet,
    so spaces should be replaced by a lowercase letter as appropriate.
    Otherwise, lower case letters should remain lower case, upper case
    letters should remain upper case, and all other punctuation should
    stay as it is.
    
    text: string to apply the shift to
    shift: amount to shift the text
    returns: text after being shifted by specified amount.

    Example:
    >>> apply_shift('This is a test.', 8)
    'Apq hq hiham a.'
    """
    ### TODO.
    return apply_coder(text, build_encoder(shift))
#
# Problem 2: Codebreaking.
#

def find_best_shift(wordlist, text):
    """
    Decrypts the encoded text and returns the plaintext.

    text: string
    returns: 0 <= int 27

    Example:
    >>> s = apply_coder('Hello, world!', build_encoder(8))
    >>> s
    'Pmttw,hdwztl!'
    >>> find_best_shift(wordlist, s) returns
    8
    >>> apply_coder(s, build_decoder(8)) returns
    'Hello, world!'
    """
    ### TODO
    # open wordlist
    # for a particular shift i >= 1
    # see if that shift produces a text whose words matche a lot of words in wordlist
    ## determine word delimiter for particular shift
    ### find " "
    ## seperate words in encrypted text
    ## decrypt each word
    ## search wordlist for each seperated word
    # save each shift's percentage of words in word list
    # compare different shift to find which shift is max percent
    ##
    maximum_coord = 0
    maximum = 0
    count = 0
    for j in range(28):
        encrypted_text = apply_coder(text, build_decoder(j))
        words_in_text = []
        chosen_word = ""
        for i in range(len(encrypted_text)):
            if encrypted_text[i] == " ":
                words_in_text.append(chosen_word)
                chosen_word = ""
            elif encrypted_text[i] == ",":
                words_in_text.append(chosen_word)
                chosen_word = ""
            elif encrypted_text[i] == ".":
                words_in_text.append(chosen_word)
                chosen_word = ""
            elif encrypted_text[i] == "!":
                words_in_text.append(chosen_word)
                chosen_word = ""
            elif encrypted_text[i] == "?":
                words_in_text.append(chosen_word)
                chosen_word = ""
            else:
                chosen_word = chosen_word + encrypted_text[i]
        words_in_text.append(chosen_word)
        for word in words_in_text:
            if word == "":
                words_in_text.remove(word)
        for word in words_in_text:
            if is_word(wordlist, word) == True:
                count = count + 1
                print word
                if word == "a":
                    count = count - 0.5
                if word == "i":
                    count = count - 0.5
                if len(word) > 3:
                    count = count + 1
                if len(word) > 4:
                    count = count + 2
                if len(word) > 5:
                    count = count + 3
                print "FBS: count", count
        if count > maximum:
             maximum = count
             maximum_coord = j
             print "FBS max: ", maximum
             print "FBS Max coord", maximum_coord
        count = 0
    return maximum_coord

def find_best_word(wordlist, text):
    maximum_coord = 0
    maximum = 0
    count = 0
    for j in range(28):
        encrypted_text = apply_coder(text, build_decoder(j))
        words_in_text = []
        chosen_word = ""
        for i in range(len(encrypted_text)):
            if encrypted_text[i] == " ":
                words_in_text.append(chosen_word)
                chosen_word = ""
            elif encrypted_text[i] == ",":
                words_in_text.append(chosen_word)
                chosen_word = ""
            elif encrypted_text[i] == ".":
                words_in_text.append(chosen_word)
                chosen_word = ""
            elif encrypted_text[i] == "!":
                words_in_text.append(chosen_word)
                chosen_word = ""
            elif encrypted_text[i] == "?":
                words_in_text.append(chosen_word)
                chosen_word = ""
            else:
                chosen_word = chosen_word + encrypted_text[i]
        words_in_text.append(chosen_word)
        for word in words_in_text:
            if word == "":
                words_in_text.remove(word)
        English_words = []
        for word in words_in_text:
            if is_word(wordlist, word) == True:
                count = count + 1
                print word
                if word == "a":
                    count = count - 0.5
                if word == "i":
                    count = count - 0.5
                English_words.append(word)
        # Find longest word in list of English words
        if count > 1:
            maximum_word = ""
            for word in English_words:
                if len(word) > len(maximum_word):
                    maximum_word = word
        if count > maximum:
             maximum = count
             maximum_coord = j
        count = 0
    return maximum_word

#
# Problem 3: Multi-level encryption.
#
def apply_shifts(text, shifts):
    """
    Applies a sequence of shifts to an input text.

    text: A string to apply the Ceasar shifts to 
    shifts: A list of tuples containing the location each shift should
    begin and the shift offset. Each tuple is of the form (location,
    shift) The shifts are layered: each one is applied from its
    starting position all the way through the end of the string.  
    returns: text after applying the shifts to the appropriate
    positions

    Example:
    >>> apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    """
    ### TODO.
    encrypted_text = []
    for letter in text:
        encrypted_text.append(letter)
    up_text = encrypted_text
    for coordinate in shifts:
        dictionary = build_encoder(coordinate[1])
        for i in range(len(text)):
            if i >= coordinate[0]:
                encrypted_text[i] = dictionary[up_text[i]]
            else:
                encrypted_text[i] = up_text[i]
        up_text = encrypted_text
    encrypted_text_string = ""
    for letter in encrypted_text:
        encrypted_text_string = encrypted_text_string + letter
    return encrypted_text_string
#
# Problem 4: Multi-level decryption.
#


def find_best_shifts(wordlist, text):
    """
    Given a scrambled string, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: Make use of the recursive function
    find_best_shifts_rec(wordlist, text, start)

    wordlist: list of words
    text: scambled text to try to find the words for
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    
    Examples:
    >>> s = random_scrambled(wordlist, 3)
    >>> s
    'eqorqukvqtbmultiform wyy ion'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> shifts
    [(0, 25), (11, 2), (21, 5)]
    >>> apply_shifts(s, shifts)
    'compositor multiform accents'
    >>> s = apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    >>> s
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> print apply_shifts(s, shifts)
    Do Androids Dream of Electric Sheep?
    """

    # beginning at start of text, search entire string for decoded shift
    # upon finding first shift, test to see if the rest of the string has actual words
    # if the rest of the string is actual words, done
    # find out at which point the actual words stop working for that shift
    ## for that shift, skip to end of word
    ## try next word
    ## if word, continue
    ## else, continue onto new shift with recursive function at the point at which the english words end
    # find out the position of the text where the english words end, call that position start
    # append that position and best shift to a list of tuples
    # search for new shift at the " " space key
    ## apply recursive function with start being the previous position and the various encryptions
    ## use apply_shifts function with wordlist, text, and list of tuples for shifts thus far discovered
    ## should look like enc_text = apply_shifts(), and then find_best_shifts_rec(wordlist, enc_text, start)
    # repeat this process until end of string
    find_best_shifts_rec(wordlist, text, 0)

t = random_scrambled(wordlist, 4)
print t
s = random_string(wordlist, 3)
v = apply_coder(s, build_encoder(3))
list_of_tuples = []
list_of_words = []
def find_best_shifts_rec(wordlist, text, start):
    """
    Given a scrambled string and a starting position from which
    to decode, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: You will find this function much easier to implement
    if you use recursion.

    wordlist: list of words
    text: scambled text to try to find the words for
    start: where to start looking at shifts
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    """
    ### TODO.
    text_trunc = ""
    for i in range(start, len(text)):
        text_trunc = text_trunc + text[i]
    print "rec: text_trunc =", text_trunc
    if text_trunc == "":
        print "END. List of words: ", list_of_words
        return list_of_tuples
    short_text_trunc = ""
    if len(text_trunc) > 15:
        for i in range(15):
            short_text_trunc = short_text_trunc + text_trunc[i]
    else:
        short_text_trunc = text_trunc
    print "rec: short_text_trunc = ", short_text_trunc
    best_shift = find_best_shift(wordlist, short_text_trunc)
    decrypted_text = apply_coder(text_trunc, build_decoder(best_shift))
    print "rec: decrypted_text = ", decrypted_text
    words_in_text = []
    chosen_word = ""
    for i in range(len(decrypted_text)):
        if decrypted_text[i] == " ":
            words_in_text.append(chosen_word)
            chosen_word = ""
            break
        else:
            chosen_word = chosen_word + decrypted_text[i]
    words_in_text.append(chosen_word)
    count = 0
    for word in words_in_text:
        if word == "":
            words_in_text.remove(word)
    print "rec: words_in_text = ", words_in_text
    if is_word(wordlist, words_in_text[0]) == True:
        print "rec: word = ", words_in_text[0]
        list_of_words.append(words_in_text[0])
        words_in_text.remove(words_in_text[0])
        best_shift_tup = (start, best_shift)
        print "rec: best_shift_tup = ", best_shift_tup
        list_of_tuples.append(best_shift_tup)
        print "rec: list_of_tuples = ", list_of_tuples
##    if is_word(wordlist, words_in_text[0]) == True:
##        print "rec: word = ", word
##        list_of_words_shift.append(word)
##        words_in_text.remove(word)
##        count += 1
##        if count < 2:
##            best_shift_tup = (start, best_shift)
##            print "rec: best_shift_tup = ", best_shift_tup
##            list_of_tuples.append(best_shift_tup)
##            print "rec: list_of_tuples = ", list_of_tuples
##    maximum_word = ""
##    for word in list_of_words_shift:
##        if len(word) > len(maximum_word):
##            maximum_word = word
##    if maximum_word != "":
##        list_of_words.append(maximum_word)
    position = start
    counter = 0
    for word in list_of_words:
        counter += 1
    if counter > 0:
        position = position + 1 + len(list_of_words[-1])
    print "rec: position = ", position
    text = apply_shifts(text, list_of_tuples)
    print "rec: encrypted_text = ", text
    find_best_shifts_rec(wordlist, text, position)

find_best_shifts_rec(wordlist, t, 0)

##find_best_shifts_rec(wordlist, get_fable_string(), 0)
##fable = ""
##for word in list_of_words:
##    fable = fable + " " + word
##print fable

def decrypt_fable():
     """
    Using the methods you created in this problem set,
    decrypt the fable given by the function get_fable_string().
    Once you decrypt the message, be sure to include as a comment
    at the end of this problem set how the fable relates to your
    education at MIT.

    returns: string - fable in plain text
    """
     find_best_shifts(wordlist, get_fable_string())
#What is the moral of the story?
#
#
#
#
#

