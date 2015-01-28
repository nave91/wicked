import os,sys,inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"pom3")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from pom3 import *

MODEL = { "pom3A": 
          {
              "LOWS" : [0.1, 0.82, 2,  0.40, 1,   1,  0, 0, 1],
              "UPS"  : [0.9, 1.20, 10, 0.70, 100, 50, 4, 5, 44]
              },
          "pom3B":
          {
              "LOWS" : [0.10, 0.82, 80, 0.40, 0,   1, 0, 0, 1],
              "UPS"  : [0.90, 1.26, 95, 0.70, 100, 50, 2, 5, 20]
          },
          "pom3C":
          {
              "LOWS" : [0.50, 0.82, 2, 0.20, 0,  40, 2, 0, 20],
              "UPS"  : [0.90, 1.26, 8, 0.50, 50, 50, 4, 5, 44]
          }
      }

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
    def __init__(self,model):
        self.collection = {}
        self.names = ["Culture", "Criticality", "CriticalityModifier", 
                      "InitialKnown", "InterDependency", "Dynamism", 
                      "Size", "Plan", "TeamSize"]   
        self.LOWS = MODEL[model]["LOWS"]
        self.UPS  = MODEL[model]["UPS"]
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
        import random
        for _ in range(N):
            t = []
            for n in self.names:
                t.append(round(random.uniform(self.collection[n].low,
                                              self.collection[n].up),2))
            inp.append(t)
        
        header,rows = pomrunner(self.names,inp,verbose)
        return header,rows

    def __repr__(self):
        return str(self.names)+'\n'+str(self.collection)+'\n'
    def __str__(self):
        return str(self.names)+'\n'+str(self.collection)+'\n'


def pomrunner(header,rows,verbose):
    return pom3_builder.pom3_csvmaker(header,rows,verbose)

def pom3d(N=50):
    os = Os()
    os.trials(100,True)
    
if __name__ == "__main__":
    pom3d()
