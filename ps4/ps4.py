def nestEggFixed(salary, save, growthRate, years):
    """
    - salary: the amount of money you make each year.
    - save: the percent of your salary to save in the investment account each
      year (an integer between 0 and 100).
    - growthRate: the annual percent increase in your investment account (an
      integer between 0 and 100).
    - years: the number of years to work.
    - return: a list whose values are the size of your retirement account at
      the end of each year.
    """
    F = [salary*save*0.01]
    for n in range(1,years):
        n = F[0] + F[n-1]*(1+0.01*growthRate)
        F.append(round(n))
    return F

def testNestEggFixed():
    salary     = 10000
    save       = 10
    growthRate = 15
    years      = 5
    savingsRecord = nestEggFixed(salary, save, growthRate, years)
    print savingsRecord
    # Output should have values close to:
    # [1000.0, 2150.0, 3472.5, 4993.375, 6742.3812499999995]
    print nestEggFixed(30000,15,5,40)
    print nestEggFixed(80000,15,5,40)
    print nestEggFixed(30000,5,5,40)
    print nestEggFixed(30000,5,10,40)

def nestEggVariable(salary, save, growthRates):
    F = [salary*save*0.01]
    for n in range(1,len(growthRates)):
        n = F[0] + F[n-1]*(1+0.01*growthRates[n])
        F.append(round(n))
    return F
    
def testNestEggVariable():
    salary      = 10000
    save        = 10
    growthRates = [3, 4, 5, 0, 3]
    savingsRecord = nestEggVariable(salary, save, growthRates)
    print savingsRecord
    # Output should have values close to:
    # [1000.0, 2040.0, 3142.0, 4142.0, 5266.2600000000002]
    print nestEggVariable(30000,15,[4,2,-3,5,6,1,3,2,0])
    print nestEggVariable(80000,15,[10,1,1,0,0,10])
    print nestEggVariable(30000,5,[1,2,3,4,5,6,7,8,9])
    print nestEggVariable(30000,5,[40])

def postRetirement(savings, growthRates, expenses):
    """
    - savings: the initial amount of money in your savings account.
    - growthRate: a list of the annual percent increases in your investment
      account (an integer between 0 and 100).
    - expenses: the amount of money you plan to spend each year during
      retirement.
    - return: a list of your retirement account value at the end of each year.
    """
    F = [savings*(1+0.01*growthRates[0])-expenses]
    for n in range(1,len(growthRates)):
        n = F[n-1]*(1+0.01*growthRates[n])-expenses
        F.append(n)
    return F    

def testPostRetirement():
    savings     = 100000
    growthRates = [10, 5, 0, 5, 1]
    expenses    = 30000
    savingsRecord = postRetirement(savings, growthRates, expenses)
    print savingsRecord
    # Output should have values close to:
    # [80000.000000000015, 54000.000000000015, 24000.000000000015,
    # -4799.9999999999854, -34847.999999999985]
    print postRetirement(300000, [0,0,1,4,4,5,3,2,-1,-1,-1,-1,2,2,2,1,1,1,1,1], 25000)
    print postRetirement(1000000, [0,0,1,4,4,5,3,2,-1,-1,2,1,1,1,1], 50000)

# guessing alg for how much expenses should be each year given variable params
# retirement until death
def findMaxExpenses(salary, save, preRetireGrowthRates, postRetireGrowthRates,
                    epsilon):
    """
    - salary: the amount of money you make each year.
    - save: the percent of your salary to save in the investment account each
      year (an integer between 0 and 100).
    - preRetireGrowthRates: a list of annual growth percentages on investments
      while you are still working.
    - postRetireGrowthRates: a list of annual growth percentages on investments
      while you are retired.
    - epsilon: an upper bound on the absolute value of the amount remaining in
      the investment fund at the end of retirement.
    """
    retirelist = nestEggVariable(salary, save, preRetireGrowthRates)
    savings = retirelist[-1]
    print savings
    ctr = 1
    low = 0
    high = savings + epsilon
    retire = [retirelist[-1]]
    while abs(retire[-1]) > epsilon and ctr <= 25:
        guess = (low+high)/2
        retire = postRetirement(savings,postRetireGrowthRates,guess)
        if retire[-1] > 0:
            low = guess
        else:
            high = guess
        guess = (low+high)/2
        ctr += 1
        print retire
    assert ctr <= 25, 'Iteration count exceeded!'
    print 'Num. iterations:', ctr, 'Estimate:', guess
    return guess

def testFindMaxExpenses():
    salary                = 10000
    save                  = 10
    preRetireGrowthRates  = [3, 4, 5, 0, 3]
    postRetireGrowthRates = [10, 5, 0, 5, 1]
    epsilon               = .01
    expenses = findMaxExpenses(salary, save, preRetireGrowthRates,
                               postRetireGrowthRates, epsilon)
    print expenses
    # Output should have a value close to:
    # 1229.95548986

    # TODO: Add more test cases here.
testFindMaxExpenses()
