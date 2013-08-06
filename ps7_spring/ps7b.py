import math
import random

def Yahtzee(trials):
    yahtzee = 0
    for i in range(trials):
        count = 0
        for j in range(5):
            if random.random() < 0.166666666666666667:
                count += 1
        if count == 5:
            yahtzee += 1
    print float(yahtzee)/float(trials)

Yahtzee(100000)

yahtzee_prob = 0.000128600823
