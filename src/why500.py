from read_jmoo import jmoo_xomo,jmoo_pom
from _preptab import display,dashedExps
from _nave_interface import tekprint

xomo_objectives = ['-effort','-months','-defects','-risks']
pom_objectives = ['-cost','+completion','-idle']

def csvprintmw(Edash,Tech,obj):
    print ",".join(obj)
    for s in ['m','w']:
        for t in Tech:
            out = [str(t)+' '+str(s)]
            for d in obj:
                out.append(int(Edash[t][d][s]))
            print ",".join([str(i) for i in out])

def _perform(model,pops,func):
    esdash = {}
    totalsize = {}
    for p in pops:
        iname = 'CT/alljresults/jmoo_'+model+str(p)+'.pickle'
        tname = str(p)#'NSGA '+str(p)
        totalsize[tname] = 20
        esdash[tname],_ = func(iname)

    return esdash,totalsize

def perform(model,pops,fname,p='csv'):
    if model in ['pom3A','pom3B','pom3C']:
        func = jmoo_pom
        obj = pom_objectives

    else:
        func = jmoo_xomo
        obj = xomo_objectives

    esdash,totalsize = _perform(model,pops,func)

    for key,es in esdash.items():
        es.calc(totalsize[key])
    Tech = sorted(totalsize.keys())
    Edash,MinP,MaxP = dashedExps(esdash,obj)
    
    if p == 'csv': csvprintmw(Edash,Tech,obj)
    #display(Edash,obj,Tech,MinP,MaxP)
    
    #tekprint(fname,Edash,obj,Tech,MinP,MaxP)

if __name__ == '__main__':
    pops = [100,200,300,400,500]
    #perform('pom3A',pops,'pom_performance.tex')
    perform('xomoal',pops,'xomo_performance.tex')
        
    
    
    
