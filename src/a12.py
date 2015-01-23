import random
from base import *
from lib  import *

def a12old(lst1,lst2,rev=True):
  "how often is x in lst1 more than y in lst2?"
  more = same = 0.0
  for x in lst1:
    for y in lst2:
      if   x==y : same += 1
      elif rev     and x > y : more += 1
      elif not rev and x < y : more += 1
  return (more + 0.5*same) / (len(lst1)*len(lst2))

def a12(lst1,lst2, gt= lambda x,y: x > y):
  "how often is x in lst1 more than y in lst2?"
  def loop(t,t1,t2): 
    while t1.i < t1.n and t2.i < t2.n:
      h1 = t1.l[t1.i]
      h2 = t2.l[t2.i]
      if gt(h1,h2):
        t1.i  += 1; t1.gt += t2.n - t2.i
      elif h1 == h2:
        t2.i  += 1; t1.eq += 1; t2.eq += 1
      else:
        t2,t1  = t1,t2
    return t.gt*1.0, t.eq*1.0
  #--------------------------
  lst1 = sorted(lst1, cmp=gt)
  lst2 = sorted(lst2, cmp=gt)
  n1   = len(lst1)
  n2   = len(lst2)
  t1   = Thing(l=lst1,i=0,eq=0,gt=0,n=n1)
  t2   = Thing(l=lst2,i=0,eq=0,gt=0,n=n2)
  gt,eq= loop(t1, t1, t2)
  return gt/(n1*n2) + eq/2/(n1*n2)

def _ab1():
  x = a12([20, # 5
          19,  # 5
          18,  # 4   1
          17,  # 3   1
          16], # 2   1
         [18,17,16,15,14])
  print ':expect',0.82,':got',x

def _ab2():
  random.seed(1)
  l1 = [random.random() for x in range(10)]
  l2 = [random.random() for x in range(10)]
  #t1 = msecs(lambda : a12(l1,l2))
  #t2 = msecs(lambda : a12old(l1,l2))
  #print ':new',t1,':old',t2
  print a12(l1,l2)

if __name__ == '__main__' : 
  #eval(cmd('_ab2()'))
  _ab2()
