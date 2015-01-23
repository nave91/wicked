from xomo import *
import os
import sys
sys.dont_write_bytecode=True

def decisions(): return [x for x in range(27)]

class Slots():
   def __init__(self, **entries): 
     self.__dict__.update(entries)

def theModel(model):
  if not model:
    model = "flight" if  len(sys.argv) <= 1 else sys.argv[1]
  return model

def xomod1(output=os.environ["HOME"]+"/tmp/xomo",
           data = "./data",
           model=None):
  model = theModel(model)
  #print model
  c = Cocomo(data + "/" + model)
  """
  x,effort = c.xy()
  print effort
  lst = c.xys(olist=True)
#  print c.bounds
  print lst[0]
  
  for i in range(0,len(c.about())): 
     k = c.about()[i]
     print "before:",k.txt,k.min,k.max
     k.update(3,3,m=c)
     print "after:",k.txt,k.min,k.max
  """   
     
  
  """
  k = filter(lambda x: x.txt == txt,c.about())[0]
  print k.txt, k.min,k.max
  k.update(1000,1600,m=c)
  
  print k.txt,k.min,k.max
  for _ in range(10):
    print "kloc", c.xys()[0]["kloc"]
  print c.xys"""
  c.xys(verbose = False)
  out = output + "/" + model + ".csv"
  #c.trials(out=out,verbose=False)
  header = ['$aa', '$sced', '$cplx', '$site', '$resl', '$acap', '$etat', '$rely', '$data', '$prec', '$pmat', '$aexp', '$flex', '$pcon', '$tool', '$time', '$stor', '$docu', '$b', '$plex', '$pcap', '$kloc', '$ltex', '$pr', '$ruse', '$team', '$pvol']
  row = [2.51, 1.0, 1.17, 1.14, 5.34, 0.84, 1.28, 1.24, 0.97, 5.77, 5.66, 0.92, 1.59, 1.14, 1.09, 1.09, 1.05, 0.97, 3.74, 1.0, 0.78, 124.96, 0.92, 1.41, 1.19, 2.23, 1.17]
  c.simulate(header,row,verbose=False)
  sys.stderr.write("# see" + out + "\n")


 
#xys ==> (listOfIndep, dep1,dep2, dep3....)

xomod1()
