#http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-00-introduction-to-computer-science-and-programming-fall-2008/assignments/pset2.pdf

##def gcd(n1,n2):
##    while n2 != 0:
##        nT = n1%n2
##        n1 = n2
##        n2 = nT
##    return n1
##
##x=60
##sol = []
##poss = []
##counter=0
##for n in range(1,x):
##    for a in range(0,10):
##        for b in range(0,7):
##            for c in range(0,3):
##                if 6*a+9*b+20*c == n:
##                    sol.append(n)
##for n in range(1,60):
##    poss.append(n)
##    if n in sol:
##        poss.remove(n)
##for p in poss:
##    print p
##print "Largest number of McNuggets that can't be bought in exact quant: ", poss[-1]

bestSoFar = 0
packages = (3,5,10)   # variable that contains package sizes
sol = []
poss = []
for n in range(1, 150):   # only search for solutions up to size 150
    for a in range(0,60):
        for b in range(0,60):
            for c in range(0,60):
                if packages[0]*a+packages[1]*b+packages[2]*c == n:
                    sol.append(n)
for n in range(1,60):
    poss.append(n)
    if n in sol:
        poss.remove(n)
for p in poss:
    print p
print "Given package sizes, " + str(packages[0]) + "," + str(packages[1]) + ", " + str(packages[2]) + ", the largest number of McNuggets that can't be bought in exact quantity is: " + str(poss[-1])
