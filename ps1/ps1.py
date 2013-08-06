#computes primes below an inputted number and computes the sum of their logs
from math import * #importing math library
n = int(raw_input("Enter #: ")) #user enters bound number
primes = [] #define empty list
for p in range(2,n+1): #runs through every prime possibility between 2 and n+1
    primes.append(p) #adds p to primes to begin with
    for c in range(2,p): #for specific p runs through c=2 to c=p
        if p%c==0 and p!=c: #checks primeness for p
            primes.remove(p) #removes p from primes list if p is not prime
            break #breaks sequence for non-primes so program doesn't remove p twice
total = 0 #bringup var total
for p in primes:
    total = total + log(p) #sums logs of each prime in list
print total
print n
print total/n
