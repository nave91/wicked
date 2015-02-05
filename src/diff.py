#Module for checking differences between clusters
#Check diff()
import os
import reader
import properties
import xy_proj
from a12 import *
from stats import *
from table import *
from xy_dt import xy_dt

#from gen import *
sys.do_not_write_bytecode = True

class Diff: 
    def __init__(self,worse,diffs,pop):
        self.worse = worse
        self.diffs = diffs
        self.pop = pop
        
    def generate(self,function,model,verbose):
        return function(self.worse,self.diffs,
                        model,n=int(self.pop),verbose=verbose)
            
    def __str__(self):
        return ">diff for: "+str(self.worse)+\
            " is: "+str(self.diffs)+" <"

    def __repr__(self):
        return ">diff for: "+str(self.worse)+\
            " is: "+str(self.diffs)+" <"

def bettercheck(one,two,verbose=False):
    
    def envy(one,two):
        # envy for decreasing obj
        yes = False
        for x,y in zip(one,two):
            if x > y: yes= True
            if x < y: return False
        return yes
        
    ones,twos = [],[]
    for fea in less[one]:
        ones.append(mu[one][fea])
        twos.append(mu[two][fea])
    for fea in more[one]:
        ones.append(mu[two][fea])
        twos.append(mu[one][fea])
    return not envy(ones,twos)

"""
def bettercheck(one,two,verbose = False):
    #both tests passed, similar
    better,similar,worse = 0,0,0
    for fea in dep[one]:
        index = colname[one].index(fea)
        y = []
        z = []
        for row in range(0,len(data[one])):
            y.append(data[one][row][index])
        for row in range(0,len(data[two])):
            z.append(data[two][row][index])
        if verbose: print fea,">>"
        a12_check = a12(y,z) < 0.6
        if a12_check:
            if verbose: print "a12 passed"
            similar += 1
        else:
            if verbose: print "a12 failed"
            #cohens_check = cohens(y,z) < 0.3
            bootstrap_check = bootstrap(y,z,b=args['bpop'])
            check = bootstrap_check#cohens_check
            if check:
                if verbose: print "bootstrap passed"
                similar += 1
            else:
                if verbose: print "bootstrap failed"
                if verbose: print mu[one][fea],mu[two][fea]
                if one in more and two in more:
                    if fea in more[one]:
                        if mu[one][fea] > mu[two][fea]:
                            better += 1
                        else:
                            worse += 1
                if one in less and two in less:
                    if fea in less[one]:
                        if mu[one][fea] < mu[two][fea]:
                            better += 1
                        else:
                            worse += 1
    if verbose: print "b",better,"s",similar,"w",worse
    if better > 0 and worse == 0:
        return True #one is better than two
"""

def closestbetter(cluster,bid,branches,better):
    #returns bid of branch having better cluster 
    #and the better cluster
    up = down = bid
    while up>=0 or down <len(branches.collection):
        if up >= 0:
            for ncluster in branches.collection[up].clusters:
                if ncluster in better:
                    return up,ncluster
            else: up -= 1
        if down < len(branches.collection):
            for ncluster in branches.collection[down].clusters:
                if ncluster in better:
                    return down,ncluster
            else: down += 1
    sys.stderr.write("WARNING: No best Branches around.\n")
    return -1,-1
            
def addotherdiffs(diffs,z):
    d = []
    dcols = []
    for i in diffs: 
        d.append(i)
        if i[0] not in dcols: dcols.append(i[0])
    for col in colname[z]:
        if col != 'C_id':
            if col not in dcols and col not in dep[z]:
                #append new condition lo < col < high 
                if args['d']:
                    mintemp = []
                    mintemp.append(col)
                    mintemp.append(False)
                    mintemp.append(buckets[col].lo[int(lo[z][col])])
                    maxtemp = []
                    maxtemp.append(col)
                    maxtemp.append(True)
                    maxtemp.append(buckets[col].hi[int(hi[z][col])])
                    d.append(mintemp)
                    d.append(maxtemp)
                else:
                    mintemp = []
                    mintemp.append(col)
                    mintemp.append(False)
                    mintemp.append(lo[z][col])
                    maxtemp = []
                    maxtemp.append(col)
                    maxtemp.append(True)
                    maxtemp.append(hi[z][col])
                    d.append(mintemp)
                    d.append(maxtemp)
    return d

def mutate(conds,wcluster,appender):
    #mutates wcluster wrt conds
    temp_data = []
    for c in conds:
        ind = colname[wcluster].index(c[0])
        for d in data[wcluster]:
            le = c[1]
            if le:
                if d[ind] <= c[2]:
                    if d not in temp_data: temp_data.append(d)
            else:
                if d[ind] > c[2]:
                    if d not in temp_data: temp_data.append(d)
    wced = wcluster+appender
    reader.makeTable(colname[wcluster],wced)
    for r in temp_data:
        reader.addRow(r,wced)
    return wced

def formatout(out):
    #Takes diff as arg and returns cleaned diff
    diffout = []
    #return only unique
    for i in out:
        if i not in diffout:
            diffout.append(i)
    out = diffout[:]
                
    #Return only non-contradicting conditions
    for i,r1 in enumerate(out):
        for j,r2 in enumerate(out):
            if r1[0] == r2[0] and r1[2] == r2[2] and r1[1] != r2[1]:
                out.pop(out.index(r1))
                out.pop(out.index(r2))
    return out

def diff(z,args,model=args['m'],verbose=False,checkeach=False):
    #Returns C1zlst as diffs added to z (main cluster) conditions
    #Returns C2zlst as diffs added to wclusters(local) conditions
    zlst,branches = xy_dt(z,args)
    #form better or worse on clusters in tree
    clus = [None]
    for _,b in branches.collection.items():
        for c in b.clusters:
            if c not in clus: clus.append(c)
    temp_zlst = zlst[:]
    zlst = clus[:]
    #Better on one if diff and less 
    #Worse on none if same
    scores = {}
    for zs in zlst[1:]:
        scores[zs] = 0
    for one in zlst[1:]:
        for two in zlst[1:]:
            if one != two:
                if bettercheck(one,two):
                    if one in scores: scores[one] += 1
                    else: scores[one] = 1
    zlst = temp_zlst[:]
    scorestuple = sorted(scores.iteritems(), key=lambda x:-x[1])
    nb = len(scores)**0.5 #Number of betters = sq_rt(len(scores)) 
    betterstuple = scorestuple[:int(nb)]
    lastbetterscore = betterstuple[-1][1]
    
    betters,worses = [],[] #List of better and worse clusters
    for i in betterstuple:
        betters.append(i[0])
    for i in scorestuple:
        if i[0] not in betters:
            worses.append(i[0])
    
    if verbose:
        print scorestuple
        print "better",betters
        print "worse",worses
        sys.exit()
    decs,incs,sames,clus = 0,0,0,0
    outdiffs = []
    C1outzlst = []
    C2outzlst = []
    import gen

    Diffs = []

    for bid,branch in branches.collection.items():
        for cluster in branch.clusters:
            if cluster in worses:
                wbid = bid
                wcluster = cluster
                bbid,bcluster = closestbetter(cluster,bid,branches,betters)
                if verbose: print "b: "+str(bcluster),",","w: "+str(wcluster)
                if bbid > -1: 
                    C2diffs = branches.difference(bbid,wbid)
                    if verbose: print diffs
                    #C2
                    appender = "C2ced"
                    
                    if args['d']:
                        C2diffs = C2diffs
                    else:
                        C2diffs = addotherdiffs(C2diffs,wcluster)
                    
                    C2diffs = formatout(C2diffs)
                    
                    C2wced = mutate(C2diffs,wcluster,appender) #before mutated
                    majclass_samples = branches.collection[wbid].samples

                    Diffs.append(Diff(C2wced,C2diffs,majclass_samples))

    return Diffs,betters,zlst,branches

def printdiffs(diffs):
    diffs.sort(key=lambda x: x[1])
    diffs.sort(key=lambda x: x[0])
    for i in diffs:
        out = ''
        out += str(i[0])
        if i[1]:
            out += ' <= '
        else:
            out += ' > '
        out += str(i[2])
        print out

if __name__ == "__main__":
    name = os.path.basename(__file__).split('.')[0]
    properties.get_args(name,args)
    #Read csvfile
    reader.pomreadFromCT()
    print diff(z,args,model=args['m'])
    sys.exit()
    if args['d']:
        import tshortener
        zlst = xy_proj.xy_proj(z,data,args) 
        zshort = tshortener.tshortener(z,zlst,colname,data,dep,indep,1.0)
        z = str(zshort)
    #differs,C1zlst,C2zlst,zlst = diff(z,args,model=args['m'])
    differs,C2zlst,zlst = diff(z,args,model=args['m'])
    #print differs
    
