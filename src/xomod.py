import os,sys,inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"xomo")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)


lows = "LOWS"
ups = "UPS"

import os
import sys
sys.dont_write_bytecode=True


def theModel(model):
  if not model:
    model = "flight"
  return model

def xomod1(output=os.environ["HOME"]+"/tmp/xomo",
           data = "../data",
           model = None):
  from xomo.xomo import Cocomo
  model = theModel(model)
  xomomap = {"xomofl" : "flight",
             "xomogr" : "ground",
             "xomoos" : "osp",
             "xomoo2" : "osp2",
             "xomoal" : "all"}
    
  model = xomomap[model]

  c = Cocomo(data + "/" + model)
  return c,model
