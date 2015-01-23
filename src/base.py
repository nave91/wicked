import sys
sys.dont_write_bytecode=True # no .pyc files
import random

#---- Cool Classes ----------------------------

class Charmed:
  "Our objects are charming."
  def __repr__(i):
    """
    This Charmed object knows how to print
    all their slots, except for the private ones
    (those that start with "_").
    """
    args = []
    for key,val in vars(i).items(): 
      if key[0] != "_":
        args += ['%s=%s'% (key,val)]
    what = i.__class__.__name__
    return '%s(%s)' % (what, ', '.join(args)) 

class Thing(Charmed):
  """Norvig's shortcut for creating objects that 
  that holds data in several fields."""
  def __init__(self, **entries): 
    self.__dict__.update(entries)

class Sample(Charmed):
  "Keep a random sample of stuff seen so far."
  def __init__(i,size=64):
    i._cache, i.size, i.n = [],size, 0.0
    i._ordered=False
  def sorted(i):
    if not i._ordered:
      i._cache = sorted(i._cache)
      i._ordered=True
    return i._cache
  def seen(i,x):
    i.n += 1
    if len(i._cache) < i.size : 
      i._cache += [x]
      i._ordered=False
    else:
      if random.random() <= i.size/i.n:
        i._cache[int(random.random()*i.size)] = x
        i._ordered=False
