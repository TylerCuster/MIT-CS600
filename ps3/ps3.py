## 2 Functions that return the number of instances of a non-overlapping
## substring in a string - 1 is iterative, 1 is recursive

from string import *
##
##def countSubStringMatch(target,key):
##    counter = 0
##    tag = 0
##    while tag < len(target):
##        pos = find(target,key,tag)
##        if pos > -1:
##            counter = counter + 1
##            tag = pos + 1
##        else: tag = tag + 1
##    return counter
##        
##def count2(target,key):
##    pos = find(target,key) #find function returns place of 1st instance of key
##    if pos >= 0: #find returns -1 if key is not in target
##        target = target[(pos+len(key)):] #if key is found, make target shorter
##        return 1 + count2(target,key) #now repeat function w/ new target
##    else: return 0

## problem 3: subStringMatchOneSub searches target with key and returns
## starting indices of key with one letter substitutions in the key
##
##def subStringMatchExact(target,key):
##    """function returns starting indices of substring in string in a tuple"""
##    tag = 0
##    l = []
##    while tag <= len(target):
##        index = find(target,key,tag)
##        if index >= 0 and index == tag:
##            l.append(index)
##        tag = tag + 1
##    tup = tuple(l)
##    return tup
##
##def constrainedMatchPair(firstMatch,secondMatch,length):
##    """gives tuple w/ n s.t. for n in tuple 1, k in tuple 2, k = n+length+1"""
##    l = []
##    for n in firstMatch:
##        for k in secondMatch:
##            if n == k - length - 1:
##                l.append(n)
##    return tuple(l)
##
##def subStringMatchOneSub(target,key):
##    """search for all locations of key in target, with one substitution"""
##    allAnswers = ()
##    for miss in range(0,len(key)):
##        # miss picks location for missing element
##        # key1 and key2 are substrings to match
##        key1 = key[:miss]
##        key2 = key[miss+1:]
##        print 'breaking key',key,'into'
##        print key1
##        print key2
##        # match1 and match2 are tuples of locations of start of matches
##        # for each substring in target
##        match1 = subStringMatchExact(target,key1)
##        match2 = subStringMatchExact(target,key2)
##        # when we get here, we have two tuples of start points
##        # need to filter pairs to decide which are correct
##        filtered = constrainedMatchPair(match1,match2,len(key1))
##        allAnswers = allAnswers + filtered
##        print 'match1',match1
##        print 'match2',match2
##        print 'possible matches for',key1,key2,'start at',filtered
##    return allAnswers
##
def subStringMatchExact(target,key):
    """function returns starting indices of substring in string in a tuple"""
    tag = 0
    l = []
    while tag <= len(target):
        index = find(target,key,tag)
        if index >= 0 and index == tag:
            l.append(index)
            tag = tag + 1
        else:
            tag = tag + 1
    tup = tuple(l)
    return tup

def constrainedMatchPair(firstMatch,secondMatch,length):
    """gives tuple w/ n s.t. for n in tuple 1, k in tuple 2, k = n+length+1"""
    l = []
    for n in firstMatch:
        for k in secondMatch:
            if n == k - length - 1:
                l.append(n)
    return tuple(l)

def subStringMatchOneSub(target,key):
    """search for all locations of key in target, with one substitution"""
    allAnswers = ()
    for miss in range(0,len(key)):
        # miss picks location for missing element
        # key1 and key2 are substrings to match
        key1 = key[:miss]
        key2 = key[miss+1:]
        print 'breaking key',key,'into'
        print key1
        print key2
        # match1 and match2 are tuples of locations of start of matches
        # for each substring in target
        lmatch = list(subStringMatchExact(target,key))
        match1 = subStringMatchExact(target,key1)
        match2 = subStringMatchExact(target,key2)
        # when we get here, we have two tuples of start points
        # need to filter pairs to decide which are correct
        filtered = constrainedMatchPair(match1,match2,len(key1))
        allAnswers = allAnswers + filtered
        print 'match1',match1
        print 'match2',match2
        print 'possible matches for',key1,key2,'start at',filtered
        print ''
    return allAnswers

