#! /usr/env python
from xy_lib import *
#from xy_globfile import *
#from maint import *
import sys #temp

class row:
    def __init__(i,row):
        i.row = row
        i.x = 0
        i.y = 0
    
    def __repr__(i):
        return "\n> x: "+str(i.x)+" y: "+str(i.y)+" "+str(i.row)

class xy:
    def __init__(i,z,pz,cols):
        i.xs=0
        i.ys=0
        i.kept=[]
        i.z = z
        i.Zofxy = "__Zofxy"
        makeTable(cols,i.z)
        i.sds = []
        i.cols = cols
        i.pz = pz

    def keep(i,xyz):
        i.kept+=[xyz]
        i.xs+=xyz.x
        i.ys+=xyz.y
        addRow(xyz.row,i.z)
        i.sds = i.getKeptSds(i.z)
        #i.sds = i.getNewKeptSds()

    def getKeptSds(i,temp_z):
        sds = []
        for c in dep[temp_z]:
            if c in nump[temp_z]:
                sds.append(sd[temp_z][c])
        return sds

    
    def checkSds(i,old,new):
        #print [int(i) for i in old],[int(i) for i in new]
        #Checks std dev and if atleast one of dep has less sd than parent dont prune
        #if all of deps have more sds than parent then prune
        cnt = 0.0
        if len(old) == 0:
            sys.stderr.write("Error: No continuous dependent variable\n") 
            sys.exit()
        if len(old) != len(new): sys.stderr.write("Error: old != new, Check your dep's\n")   
        for i,j in zip(old,new):
            if i<j: cnt += 1
        if cnt > len(old)/2: return True
        else: return False
        

    def tiles(i,more,mini,oldn,spy,prune,verbose=True,lvl=0):
            
        n = len(i.kept)
        repeat = True
        sdcheck = False
        if n != 0:
            xmu = i.xs*1.0/n
            ymu = i.ys*1.0/n
        #print n,xmu,ymu
        if spy and n!=0:
            print '|--'*lvl+str(n)#,"xmuymu:",xmu,ymu
        if int(n) == int(oldn) or int(n) == 0 :
            repeat = False
            if int(n) != 0:
                if verbose>0: print "repeat yielding",len(i.kept)
                if prune: 
                    if i.pz != '': 
                        sdcheck = i.checkSds(i.getKeptSds(i.pz),i.sds)
                    else: sdcheck = False
                else:
                    yield i.kept
                if sdcheck: 
                    if verbose > 0: print "Not yielded"
                    i.kept = []
                    n = 0
                    repeat = False
                else:
                    yield i.kept
        oldn = n
        if repeat == True:
            if n>mini:
                if n<more:
                    if verbose>0: print "actual yielding",len(i.kept)
                    if prune: 
                        if i.pz != '': 
                            sdcheck = i.checkSds(i.getKeptSds(i.pz),i.sds)
                        else: sdcheck = True
                        if sdcheck: 
                            if verbose > 0: print "Not yielded"
                            i.kept = []
                            n = 0
                        else:
                            yield i.kept
                    else:
                        yield i.kept
                else:
                    hh = i.__class__(i.z+str(lvl)+'hh',i.z,i.cols)
                    hl = i.__class__(i.z+str(lvl)+'hl',i.z,i.cols)
                    lh = i.__class__(i.z+str(lvl)+'lh',i.z,i.cols)
                    ll = i.__class__(i.z+str(lvl)+'ll',i.z,i.cols)
                    for xyz in i.kept:
                        if xyz.x < xmu:
                            if xyz.y < ymu:
                                what = ll
                            else:
                                what = lh
                        else:
                            if xyz.y < ymu:
                                what = hl
                            else:
                                what = hh
                        what.keep(xyz)
                    quads = [ll,lh,hl,hh]
                    for xy in quads:
                        for one in xy.tiles(more,mini,oldn,spy,prune,verbose,lvl+1):
                            yield one
            else:
                if verbose>0: print "else yielding",len(i.kept)
                if prune: 
                    if i.pz != '': 
                        sdcheck = i.checkSds(i.getKeptSds(i.pz),i.sds)
                    else: sdcheck = False
                    if sdcheck: 
                        if verbose > 0: print "Not yielded"
                        i.kept = []
                        n = 0
                        repeat = False
                    else:
                        yield i.kept
                else:
                    yield i.kept

#########--EXTRAS--##########
"""
    def doJoin(i,quads):
        ret = False
        for quad in range(0,len(quads)-1):
            if i.checkSds(quads[quad].getNewKeptSds(),quads[quad+1].getNewKeptSds()):
                ret = True
                return ret
        if i.checkSds(quads[0].getNewKeptSds(),quads[len(quads)-1]):
            ret = True
        return ret

    def getNewKeptSds(i):
        makeTable(colname[i.z],"__xytemp")
        for r in i.kept:
            addRow(r.row,"__xytemp")
        temp = i.getKeptSds("__xytemp")
        removeTable("__xytemp")
        return temp

    def checkSds(i,new,old):
        print new,old
        #Checks std dev and if new-old < 0.3*new then returns True
        #True if they are similar,False if they are not
        cnt = 0.0
        if len(old) == 0:
            sys.stderr.write("Error: No continuous dependent variable\n") 
            sys.exit()
        if len(old) != len(new): sys.stderr.write("Error: old != new, Check your dep's\n")   
        for i,j in zip(new,old):
            one = max(i,j)
            two = min(i,j)
            if (one-two) < 0.3*one: cnt += 1
        print cnt/len(old),"##"
        if cnt/len(old) > 0.5: return True 
        else: return False

"""
"""
        if prune:
            if not sdcheck: 
                if verbose>0: print len(i.kept),"sdchecked gone!"
                repeat = False
                i.kept = []
                i.xs = 0
                i.ys = 0
                n = len(i.kept)
"""
