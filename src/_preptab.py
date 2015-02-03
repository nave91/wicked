import time
import properties,reader,xy_proj
from lib import *
from diff import diff

chops = [0.25,0.5,0.75,1.0]

class E:
    def __init__(self,c):
        self.col = c
        self.stats = {}
        self.size = 0

    def fillIn(self,m,q,w,s,l):
        self.stats['m'] = m
        self.stats['q'] = q
        self.stats['w'] = w
        self.stats['s'] = s
        self.size = l

    def __repr__(self):
        return '[ colname:'+str(self.col)+' '+str(self.stats)+']'

class Es:
    def __init__(self):
        self.collection = {}
        self.colstats = {}

    def add(self,e,zname):        
        if zname in self.collection.keys():
            self.collection[zname][e.col] = e
        else:
            self.collection[zname] = {}#.append(exp)
            self.collection[zname][e.col] = e
        
    def show(self):
        for key,value in self.collection.items():
            print 'T: '+str(key)
            print value,'\n'
    
    def calc(self,totalsize):
            for zname,dicte in self.collection.items():
                for c,e in dicte.items():
                    if c in self.colstats.keys():
                        self.colstats[c]['m'] += ((e.stats['m']*e.size)/totalsize)
                        self.colstats[c]['q'] += ((e.stats['q']*e.size)/totalsize)
                        self.colstats[c]['w'] += ((e.stats['w']*e.size)/totalsize)
                        self.colstats[c]['s'] += ((e.stats['s']*e.size)/totalsize)
                    else:
                        self.colstats[c] = {}
                        self.colstats[c]['m'] = ((e.stats['m']*e.size)/totalsize)
                        self.colstats[c]['q'] = ((e.stats['q']*e.size)/totalsize)
                        self.colstats[c]['w'] = ((e.stats['w']*e.size)/totalsize)
                        self.colstats[c]['s'] = ((e.stats['s']*e.size)/totalsize)
            return self.colstats        
    def __repr__(self):
        return str(self.colstats)
    
def mqwptiles(ptiles,z,c):
    m = medianOf(z,c)
    q = round(ptiles[c][0.75] - ptiles[c][0.25],2)
    w = ptiles[c][1.0]
    s = ptiles[c][0.25]
    return m,q,w,s

def mqwZlst(zlst,chops):
    es = Es()
    l = 0
    for i in zlst:
        l = len(data[i])
        ptiles0 = depsptile(i,chops) 
        #printptiles(i,ptiles0,chops) #To check uncomment
        for c in dep[i]:
            e0 = E(c)
            m,q,w,s = mqwptiles(ptiles0,i,c)
            e0.fillIn(m,q,w,s,l)
            #print e0 #To check uncomment
            es.add(e0,i)
    return es

def buildEs(mqws,objectives,Tname):
    es = Es()
    for _o,o in enumerate(objectives):
        e0 = E(o)
        m,q,w,s = avgmqw(mqws,_o)
        e0.fillIn(m,q,w,s,len(mqws))
        es.add(e0,Tname)
    return es

def avgmqw(mqws,_o):
    avg = []
    for _i in ['m','q','w','s']:
        s = 0
        for _mqw in mqws:
            s += _mqw[_i][_o]
        avg.append(s/len(mqws))
    assert(len(avg) == 4) #m,q,w,s
    return avg[0],avg[1],avg[2],avg[3]

def divByN(es,l):
    for c,stats in es.colstats.items():
        for key,value in stats.items():
            value = round(value/totalsize,1)
    return es

def dashedExps(esdash,deps):
    maxP,minP = {},{}
    for d in deps:
        maxP[d] = -100000
        minP[d] = 1000000
        temp = []
        for s in ['m','q','w','s']:
            for key,es in esdash.items():
                temp.append(es.colstats[d][s])
                if max(temp) > maxP[d]: maxP[d] = round(max(temp),2)
                if min(temp) < minP[d]: minP[d] = round(min(temp),2)
    Edash = {}
    for key,es in esdash.items():
        if key not in Edash.keys(): Edash[key] = {}
        for d in deps:
            if d not in Edash[key].keys(): Edash[key][d] = {}
            for s in ['m','q','w','s']:
                Ex = round(es.colstats[d][s],2)
                Edash[key][d][s] = round(100*(Ex - minP[d])/(maxP[d] - minP[d])) 
    return Edash,minP,maxP
    
def display(Edash,deps,MinP,MaxP):
    Tech = sorted(Edash.keys())
    rows = []
    d0 = MinP
    d100 = MaxP
    list100 = ["100"]
    list0 = ["0"]
    header = ["Techniques"]
    for d in deps:
        header.append(d)
    from table import rowprint
    rows.append(rowprint(header))
    print rowprint(header)
    #l = len(zlst) - 1
    for s in ['m','q','w']:
        for t in Tech:
            out = [str(t)+' '+str(s)]
            for d in deps:
                out.append(int(Edash[t][d][s]))
            rows.append(rowprint(out))
            print rowprint(out)
        print '-'*85
        rows.append('--'*60)
    for d in deps:
        list0.append(d0[d])
        list100.append(d100[d])
    rows.append(rowprint(list100))
    rows.append(rowprint(list0))
    return rows

def wrbranch(bname,Tname,nodes,leaves):
    from _nave_interface import ct_storeinfile
    ct_storeinfile(bname,[Tname.replace(" ","")
                          +":"
                          +str(nodes)
                          +":"
                          +str(leaves)])
 
   
def retreivemqws(colstats,objectives):
    m,q,w,s = 'm','q','w','s'
    mqws = {m:[], q:[], w:[], s:[]}
    for _i in [m,q,w,s]:
        for _o in objectives:
            mqws[_i].append(colstats[_o][_i])
    return mqws

def learn(z,st,nodleas,base=False):
    nodes,leaves = nodleas[0],nodleas[1]
    if args['d'] or args['i'] > 0 and not base:
        #To discretize or prune with infogain
        import tshortener
        zlst = xy_proj.xy_proj(z,data,args)
        zshort = tshortener.tshortener(z,zlst,colname,data,
                                       dep,indep,args['i'],args['d'])
        Diffs,betters,zlst,branches = diff(zshort,args)
        endtime = time.time() - st
        from gen import genwithdiffs,smartsamples
        #T3zlst = genwithdiffs(Diffs,betters,args['m'],verbose=False)
        T3zlst = smartsamples(Diffs,betters,args['m'],verbose=False)
        nodes += branches.nodes
        leaves += branches.leaves
    elif not base:
        # Just plain CT no prune
        Diffs,betters,zlst,branches = diff(z,args)
        endtime = time.time() - st
        from gen import genwithdiffs,smartsamples
        #T3zlst = genwithdiffs(Diffs,betters,args['m'],verbose=False)
        T3zlst = smartsamples(Diffs,betters,args['m'],verbose=False)
        nodes += branches.nodes
        leaves += branches.leaves
    else:
        #Base
        T0zlst = xy_proj.xy_proj(z,data,args)
        T3zlst = T0zlst[1:]
        endtime = time.time() - st
    

    es = mqwZlst(T3zlst,chops)
    newrows = []

    for i in T3zlst:
        newrows += data[i]
    
    return es,mqw,endtime,(nodes,leaves),newrows

def runner(z,args,esdash,totalsize,Tname,objectives,pop,base=False,read=False):
    mqws = []
    nodleas = (0,0)
    endtimes = []
    _st = time.time()
    _r = 0
    
    while _r < args['repeats']:
        _g = 0
        if not read:
            sys.stderr.write("# loading population.\n")
            objectives = loadPopulation(z,args,pop)
        while _g < args['gens']:
            resetSeed(_r)
            st = time.time()

            es,mqw,endtime,nodleas,newrows = learn(z,st,
                                                   nodleas,base=base)
        
            reader.makeTable(colname[z],zout)
            for r in newrows:
                reader.addRow(r,zout)
            
            reader.removeTable(z)
            reader.copyTable(zout,z)
            reader.removeTable(zout)

            #Clean everything up 
            for key,value in data.items():
                if key not in [z,zout]: 
                    reader.removeTable(key)

            _g+=1

        
        # calculate es
        colstats = es.calc(len(newrows))
        mqw = retreivemqws(colstats,objectives)
        mqws.append(mqw)
        endtimes.append(endtime)

        #clean everything
        for key,value in data.items():
            if key not in [z]:
                reader.removeTable(key)
        _r += 1



                                    
    es = buildEs(mqws,objectives,Tname)
    esdash[Tname] = es
    totalsize[Tname] = args['repeats']*args['gens']
    endtime = sum(endtimes)+_st
    nodleas = (nodleas[0]/totalsize[Tname],nodleas[1]/totalsize[Tname])
    return esdash,totalsize,endtime,nodleas
        

def loadPopulation(z,args,pop):
    if args['m'] in POMPROB:
        names = ["$Culture", "$Criticality", 
                 "$CriticalityModifier", 
                 "$InitialKnown", "$InterDependency", "$Dynamism", 
                 "$Size", "$Plan", "$TeamSize",
                 '-cost','+completion','-idle']        
        from pom3d import Os
        os = Os(args['m'],names[:-3])
        header,rows = os.trials(pop)
        reader.makeTable(header,z)
        for r in rows:
            reader.addRow(r,z)
        objectives = names[-3:]
    elif args['m'] in XOMOPROB:
        from xomo import xomo_builder
        header = ['?aa','$sced','$cplx','$site','$resl','$acap',
                  '$etat','$rely','$data','$prec','$pmat','$aexp',
                  '$flex','$pcon','$tool','$time','$stor','$docu',
                  '?b','$plex','$pcap','+kloc','$ltex','$pr','$ruse',
                  '$team','$pvol','-effort','-months',
                  '-defects','-risks']
        rows = xomo_builder.trials(args['m'],pop)
        reader.makeTable(header,z)
        for r in rows:
            reader.addRow(r,z)
        objectives = ['+kloc','-effort','-defects','-months','-risks']
    elif args['m'] in DTLZPROB:
        from dtlzd import Os
        init_dtlz = Os(args['m'],args['objind'])
        header,rows = init_dtlz.trials(pop)
        reader.makeTable(header,z)
        for r in rows:
            reader.addRow(r,z)
        objectives = [i for i in header[-args['objind'][0]:]]
    return objectives
            
def ct_storeinfile(fname,output):
    sys.stderr.write("#writing into file "+fname+"\n")
    with open(fname,'ab') as f:
        for line in output:
            f.write("%s\n" % line) 
        f.close()
    
def tekprint(fname,Edash,deps,MinP,MaxP):
    Tech = sorted(Edash.keys())
    d0 = MinP
    d100 = MaxP
    list100 = ["100",""]
    list0 = ["0",""]
    header = ["Techniques","mqw"]
    for d in deps:
        header.append(d)
    l = len(Edash.keys())
    rows = []
    for s in ['m','q','w']:
        for t in Tech:
            out = [str(t)+' & '+str(s)]
            for d in deps:
                out.append(int(Edash[t][d][s]))
            rows.append(out)
    for d in deps:
        list0.append(d0[d])
        list100.append(d100[d])
    def jin(lst):
        return " & ".join([str(i) for i in lst])+" \\\\"
    writeout = ""
    writeout += jin(header)+" \hline \n"
    rs = ''
    for _r,r in enumerate(rows):        
        if r == rows[-1]:
            rs += jin(r)+' \hline \n'
        else:
            if (_r)%l == int(l)-1:
                rs += jin(r)+' \hline \n'
            else:
                rs += jin(r)+'\n'
                
    writeout += rs
    writeout += jin(list100)+"\n"
    writeout += jin(list0)+" \hline"
    ct_storeinfile(fname,[writeout])

def quartekprint(fname,Edash,deps,MinP,MaxP):
    Tech = sorted(Edash.keys())
    Tech1 = ['0','W','N']
    d0 = MinP
    d100 = MaxP
    header = ["","Rx","Median",""]
    l = len(Edash.keys())
    rows = []
    writeout = ''
    scriptstring = '\\begin{tabular}'+\
                   '{|l@{~}c@{~}c@{~}r|}'+\
                   '\n'+'\\arrayrulecolor{lightgray}\n'
    
    writeout += scriptstring
    writeout += '\\rowcolor[gray]{0.85}  '+' & '.join(header)+'\\\\ \n'
    for d in deps:

        writeout += '\\hline\\rowcolor[gray]{1.0} '+str(d[1:])+' '
        for _t,t in enumerate(Tech):
            tmp = [Tech1[_t]]
            writeout += ' & '
            for _m in ['m']:
                tmp.append(str(int(Edash[t][d][_m])))
            tmp.append('\\quart{'+str(Edash[t][d]['s'])+'}'+\
                       '{'+str(Edash[t][d]['q'])+'}'+\
                       '{'+str(Edash[t][d]['m'])+'}')
            writeout += ' & '.join(tmp)+' \\\\ \n'
        
    writeout+='\\end{tabular}'+'\n'
    ct_storeinfile(fname,[writeout])

"""
def quartekprintbig(fname,Edash,deps,MinP,MaxP):
    Tech = sorted(Edash.keys())
    Tech1 = ['Base Line','CT0','NSGA II']
    d0 = MinP
    d100 = MaxP
    header = ["Objective","method","median","IQR",""]
    l = len(Edash.keys())
    rows = []
    writeout = ''
    scriptstring = '{\\scriptsize \\begin{tabular}'+\
                   '{l@{~~~}l@{~~~}l@{~~~}r@{~~~}r@{~~~}c}'+\
                   '\n'+'\\arrayrulecolor{darkgray}\n'
    
    writeout += scriptstring
    writeout += '\\rowcolor[gray]{.7}  '+' & '.join(header)+'\\\\ \n'
    for d in deps:

        out = []
        writeout += '\\rowcolor[gray]{.9} '+str(d[1:])+' '
        for _t,t in enumerate(Tech):
            tmp = [Tech1[_t]]
            writeout += ' & '
            for _m in ['m','q']:
                tmp.append(str(int(Edash[t][d][_m])))
            tmp.append('\\quart{'+str(Edash[t][d]['s'])+'}'+\
                       '{'+str(Edash[t][d]['q'])+'}'+\
                       '{'+str(Edash[t][d]['m'])+'}')
            writeout += ' & '.join(tmp)+' \\\\ \n'
    writeout+='\\end{tabular}}'+'\n'
    ct_storeinfile(fname,[writeout])
"""
