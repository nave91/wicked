import random

def bootstrap(y0,z0,conf=0.05,b=1000):
    """The bootstrap hypothesis test from
    p220 to 223 of Efron's book 'An
    introduction to the boostrap."""
    class total():
        "quick and dirty data collector"
        def __init__(i,some=[]):
            i.sum = i.n = i.mu = 0 ; i.all=[]
            for one in some: i.put(one)
        def put(i,x):
            i.all.append(x);
            i.sum +=x; i.n += 1; i.mu = float(i.sum)/i.n
        def __add__(i1,i2): return total(i1.all + i2.all)
    def testStatistic(y,z): 
        """Checks if two means are different, tempered
        by the sample size of 'y' and 'z'"""
        tmp1 = tmp2 = 0
        for y1 in y.all: tmp1 += (y1 - y.mu)**2 
        for z1 in z.all: tmp2 += (z1 - z.mu)**2
        if y.n > 1: s1    = float(tmp1)/(y.n - 1) 
        else:       s1    = float(tmp1) #changed_nave
        if z.n > 1: s2    = float(tmp2)/(z.n - 1)
        else:       s2    = float(tmp2) #changed_nave
        delta = z.mu - y.mu
        if s1+s2:
            delta =  delta/((s1/y.n + s2/z.n)**0.5)
        return delta
    def one(lst): return lst[ int(any(len(lst))) ]
    def any(n)  : return random.uniform(0,n)
    y, z   = total(y0), total(z0)
    x      = y + z
    tobs   = testStatistic(y,z)
    yhat   = [y1 - y.mu + x.mu for y1 in y.all]
    zhat   = [z1 - z.mu + x.mu for z1 in z.all]
    bigger = 0.0
    for i in range(b):
        if testStatistic(total([one(yhat) for _ in yhat]),
                         total([one(zhat) for _ in zhat])) > tobs:
            bigger += 1
    return bigger / b < conf

def cohens(y,z):
    #cohens d=(x1-x2)/s
    x1 = sum(y)/len(y)
    x2 = sum(z)/len(z)
    yz = y+z
    avg = sum(yz)/len(yz)
    sums = 0
    for i in yz:
        sums += (avg-i)**2
    stdev = (sums/len(yz))**0.5
    return abs(x1-x2)/stdev
    
    
