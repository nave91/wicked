#Reads jmoo summary table and imports results 
import sys
import pickle 
from lib import *
from _preptab import *

m,q,w,g,s = 'm','q','w','g','s'
_mqw = ['m','q','w','s']

def rebuild_mqws_pom3(mqws):
    for _k,mqw in enumerate(mqws):
        for _i in _mqw:
            mqws[_k][_i] = mqw[_i][:1]+mqw[_i][2:]
    return mqws

def jmoo_xomo(jm):
    args['jmoo'] = jm 
    objectives = ['+kloc','-effort','-months','-defects','-risks']
    with open(jm,'r') as picklefile:
        mqws = pickle.load(picklefile)
    #get avg gens
    gens = []
    for i in mqws: gens.append(i[g])
    avggens = sum(gens)/len(gens)
    #removing gens from mqws
    for _k,mqw in enumerate(mqws):
        mqws[_k] = { key: mqw[key] for key in _mqw}
    return buildEs(mqws,objectives,Tname='jmoo'),avggens

    
def jmoo_pom(jm):
    args['jmoo'] = jm
    objectives = ['-cost','+completion','-idle']
    with open(jm,'r') as picklefile:
        mqws = pickle.load(picklefile)
    mqws = rebuild_mqws_pom3(mqws)
    #get avg gens
    gens = []
    for i in mqws: gens.append(i[g])
    avggens = sum(gens)/len(gens)
    #removing gens from mqws
    for _k,mqw in enumerate(mqws):
        mqws[_k] = { key: mqw[key] for key in _mqw}
    return buildEs(mqws,objectives,Tname='jmoo'),avggens

def moea_dtlz(z):
    pop = indepdata(z)
    _deps = len(dep[z])
    from moea import Moea
    _moea = Moea(indeps=len(indep[z]),
                 deps=len(dep[z]))
    pop = _moea.loadPopulation(pop)

    mqws,gens = [], []
    for r in range(args['repeats']):
        sys.stderr.write("# Repeating NSGAII "+str(r)+" th time\n")
        pop,logbook = _moea.runNSGAII(pop)
        #get last generation's mqw
        _lastlog = logbook[-1]
        m,q,w = 'm','q','w'
        _mqw = {m:[], q:[], w:[]}
        _mqw[m] = list(_lastlog['med'])
        _mqw[w] = list(_lastlog['max'])
    
        #for mqws[q]
        deps = []
        for _d in range(_deps):
            deps.append([p.fitness.values[_d] for p in pop])
            
        _mqw[q] = [spread(d) for d in deps]
        mqws.append(_mqw)
        gens.append(len(logbook))
        
    if len(gens)>0: avggens = sum(gens)/len(gens)
    else: print "Error: check avggens in read_jmoo. Generations= NULL"
    
    del _moea

    return buildEs([_mqw],dep[z],Tname='nsga'),avggens
    
if __name__ == '__main__':
    
    print jmoo_xomo(sys.argv[1])
    
    #moea_dtlz()
