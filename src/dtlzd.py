import sys
from deap import benchmarks
import array, random
INDOBJ = { 2 :
           { "IND" : 5,
             "OBJ" : 2},
           4 :
           { "IND" : 40,
             "OBJ" : 4},
           6 :
           { "IND" : 60,
             "OBJ" : 6},
           8 :
           { "IND" : 80,
             "OBJ" : 8}
       }
MODEL = { "dtlz1" : benchmarks.dtlz1,
          "dtlz2" : benchmarks.dtlz2,
          "dtlz3" : benchmarks.dtlz3,
          "dtlz4" : benchmarks.dtlz4}


DTLZ_LOW = 0 #Domain low of parameters
DTLZ_UP = 1  #Domain high of parameters
    
class O:
    def __init__(self,name):
        self.name = name
        self.up = 0
        self.low = 0
    
    def update(self,low,up):
        self.low = low
        self.up = up
    
    def __repr__(self):
        s = str(self.low)+' < '+self.name +' < '+str(self.up)+'\n'
        return s

class Os:
    def __init__(self,model,objind,names=None):
        self.collection = {}
        self.model = model
        self.modelFunction = MODEL[model]
        self.obj = objind[0]
        self.ind = objind[1]
        if names: self.names = names
        else:
            self.names = ['ind'+str(i) for i in range(self.ind)]
        self.LOWS = [DTLZ_LOW for _ in self.names]
        self.UPS  = [DTLZ_UP for _ in self.names]
        for _n,n in enumerate(self.names):
            self.collection[n] = O(n)
            self.collection[n].update(self.LOWS[_n],self.UPS[_n])

    def update(self,fea,cond,thresh):
        ind = self.names.index(fea)
        if cond:
            self.collection[fea].update(self.LOWS[ind],thresh)
        else:
            self.collection[fea].update(thresh,self.UPS[ind])

        
    def trials(self,N,verbose=False):
        inp = []
        out = []
        rows = []
        import random
        for _ in range(N):
            t = []
            for n in self.names:
                t.append(round(random.uniform(self.collection[n].low,
                                              self.collection[n].up),2))
            inp.append(t)
        
        #inp = [map(int,inp[i]) for i in range(len(inp))] #converts to int
        for i in range(len(inp)):
            rows.append(inp[i]+self.modelFunction(inp[i],self.obj)) 
        header = self.names + ['-obj'+str(i) for i in range(self.obj)]
        return header,rows

    def __str__(self):
        return 'dtlz'+str(self.model)+":"+str(self.ind)\
            +":"+str(self.obj)

if __name__ == "__main__":
    os = Os("dtlz1",2)
    print os
    print os.trials(10)
