import os,time
from _preptab import *

class Interface:
    def __init__(self,algo,prob,pop,rname,pname,jname,nlname,tname,dname,jtname='',objind=-1):
        self.rname = rname
        self.pname = pname
        self.jname = jname
        self.nlname = nlname
        self.tname = tname
        self.dname = dname
        self.jtname = jtname
        self.algo = algo
        self.prob = prob
        self.pop  = pop
        self.starttime = {}
        self.endtime = {}
        if self.prob in DTLZPROB:
            args['objind'] = objind
            self.objind = objind
        else:
            args['objind'] = ['_','_']
            self.objind = ['_','_']
        self.obj = self.objind[0]
        self.ind = self.objind[1]

    def gettime(self,Tname,actual=False):
        if actual:
            return round((self.endtime[Tname] - 
                           self.starttime[Tname])*1000,2)
        return [Tname+
                ":"+
                str(round((self.endtime[Tname] - 
                           self.starttime[Tname])*1000,2))] 

    def writefile(self,Tname,nodlea=None,avggens=None):
        nodes = nodlea[0]/args['repeats']
        leaves = nodlea[1]/args['repeats']
        wrbranch(self.nlname,Tname,nodes,leaves)
        
        ct_storeinfile(self.tname,self.gettime(Tname))
        ct_storeinfile(self.dname,[">> Time(min) taken by "+\
                                   str(Tname)+" for "+\
                                   str(args['repeats'])+": "+\
                                   str(self.gettime(Tname,
                                                    actual=True)/60000)])
        if nodlea[0] > 0 and nodlea[1] > 0:
            ct_storeinfile(self.dname,[">> Size of "+str(Tname)+\
                                       " is nodes: "+str(nodes)+\
                                       "\n>>\t\t\t  leaves: "+\
                                       str(leaves)])
        if avggens:
            ct_storeinfile(self.dname,[">> Average no. of gens of "+\
                                       str(Tname)+" is: "+\
                                       str(avggens)])
    

    def callrunner(self,Tname,z,args,esdash,totalsize,objectives,base=False):
        
        if self.prob in DTLZPROB:
            Tname = Tname+str(self.prob)+str(self.pop)+'p'+\
                    str(self.obj)+'o'+\
                    str(self.ind)+'i'
        else:
            Tname = Tname+str(self.prob)+str(self.pop)+'p'
            
        self.starttime[Tname] = time.time()
        print ">>>>>"*10,Tname,"<<<<<"*10
        esdash,totalsize,endtime,nodlea = runner(z,args,esdash,
                                                 totalsize,Tname,objectives,base)
        self.endtime[Tname] = endtime
        self.writefile(Tname,nodlea)

    def run(self):

        z = "main"
        esdash = {}
        totalsize = {}

        #TUNE RIG ACCORDING TO MODEL and READ INITIAL POPULATION
        if self.prob in POMPROB:
            csvfile = open(self.pname,'r')
            from pom3 import pom3_builder
            header,rows = pom3_builder.builder(csvfile)
            #Use header[:-4] to avoid extra column names in input from jmoo
            header,rows = pom3_builder.pom3_csvmaker(header[:-4],rows,
                                                         verbose=False)
            objectives = ['-cost','+completion','-idle']
            csvfile.close()
        
        elif self.prob in XOMOPROB:
            csvfile = open(self.pname,'r')
            from xomo import xomo_builder
            header,rows = xomo_builder.builder(csvfile)
            #Use header[:-4] to avoid extra column names in input from jmoo
            header,rows = xomo_builder.xomo_csvmaker(self.prob,header[:-4],rows,
                                                         verbose=False)
            
            #header,rows = xomo_builder.oldbuilder(self.prob,self.pop)
            objectives = ['-effort','-months','-defects','-risks']
            csvfile.close()
            
        elif self.prob in DTLZPROB:
            if not os.path.isfile(self.pname):
                from dtlzd import Os
                init_dtlz = Os(self.prob,self.objind)
                header,rows = init_dtlz.trials(self.pop)
                objectives = header[-self.obj:] #collect all dynamic num of objs
                #ALL OBJS are MINIMIZED == negative o below
                objectives = [ '-'+o for o in objectives] 
                header = header[:-self.obj]+objectives
                
        else:
            print "Wrong model"
            sys.exit()

        
        #Load initial Population
        reader.makeTable(header,z)
        for r in rows: reader.addRow(r,z)
        N = int(len(data[z])**0.5)
        

        #Default Configuration
        args['l'] = 0.5*N #leaf size
        args['n'] = -1 #Use all
        args['spy'] = True
        args['m'] = self.prob
        args['bpop'] = 250

        
        #Base line
        Tname = 'BL '
        args['n'] = -1
        args['l'] = 20
        args['d'] = False
        args['i'] = -1
        args['p'] = False
        self.callrunner(Tname,z,args,esdash,
                        totalsize,objectives,base=True)
        
        #CT0 SMall Tree
        Tname = 'CT0 '
        args['dtreeprune'] = True
        args['distprune'] = False
        args['d'] = True
        args['i'] = 0.75
        args['p'] = False
        args['fayyad'] = False
        args['n'] = -1 ###changed to 0.5
        self.callrunner(Tname,z,args,esdash,
                        totalsize,objectives)
        
        #CT1 Big Tree
        Tname = 'CT1 '
        args['dtreeprune'] = True
        args['distprune'] = False
        args['d'] = False
        args['i'] = -1
        args['p'] = False
        args['fayyad'] = False
        args['n'] = -1
        self.callrunner(Tname,z,args,esdash,
                        totalsize,objectives)
        
        #NSGA
        if self.prob in POMPROB:

            from read_jmoo import jmoo_pom
            
            Tname = 'NSGA '+str(self.prob)+str(self.pop)+'p'
            print ">>>>>"*10,Tname,"<<<<<"*10
            #update time from jmoo
            self.starttime[Tname] = 0
            timefile = open(self.jtname,'r')
            self.endtime[Tname] = float(timefile.readline())
            totalsize[Tname] = 20
            esdash[Tname],avggens = jmoo_pom(self.jname)
            self.writefile(Tname,[-args['repeats'],-args['repeats']],avggens=avggens)
            
        elif self.prob in XOMOPROB:

            from read_jmoo import jmoo_xomo
            
            Tname = 'NSGA '+str(self.prob)+str(self.pop)+'p'
            print ">>>>>"*10,Tname,"<<<<<"*10
            #update time from jmoo
            self.starttime[Tname] = 0
            timefile = open(self.jtname,'r')
            self.endtime[Tname] = float(timefile.readline())
            totalsize[Tname] = 20
            esdash[Tname],avggens = jmoo_xomo(self.jname)
            self.writefile(Tname,[-args['repeats'],-args['repeats']],avggens=avggens)
            
        elif self.prob in DTLZPROB:
            
            from read_jmoo import moea_dtlz
            
            Tname = 'NSGA '+str(self.prob)+str(self.pop)+'p'+\
                    str(self.obj)+'o'+\
                    str(self.ind)+'i'
            print ">>>>>"*10,Tname,"<<<<<"*10
            self.starttime[Tname] = time.time()
            totalsize[Tname] = args['repeats']
            esdash[Tname],avggens = moea_dtlz(z)
            self.endtime[Tname] = time.time()
            self.writefile(Tname,[-args['repeats'],-args['repeats']],avggens=avggens)

        for key,es in esdash.items():
            es.calc(totalsize[key])
        Tech = sorted(totalsize.keys())
        
        Edash,MinP,MaxP = dashedExps(esdash,dep[z])
        
        tekprint(self.rname,Edash,dep[z],MinP,MaxP)
        #quartekprint(self.rname,Edash,dep[z],MinP,MaxP)
        rows = display(Edash,dep[z],MinP,MaxP)
        ct_storeinfile(self.dname,rows)



"""
        #CT1 Big Tree
        Tname = 'CT1_'+str(self.prob)+str(self.pop)
        self.starttime[Tname] = time.time()
        print ">>>>>"*10,Tname,"<<<<<"*10
        totalsize[Tname] = 0
        args['dtreeprune'] = True
        args['distprune'] = False
        args['d'] = False
        args['i'] = -1
        args['p'] = False
        args['fayyad'] = False
        esdash,totalsize,endtime,nodlea = runner(z,args,esdash,
                                  totalsize,Tname,objectives)                    
        self.endtime[Tname] = endtime
        ct_storeinfile(self.tname,self.gettime(Tname))
        
        
        #CT0* Fayyad on SMall Tree
        Tname = 'CT0*_'+str(self.prob)+str(self.pop)
        self.starttime[Tname] = time.time()
        print ">>>>>"*10,Tname,"<<<<<"*10
        totalsize[Tname] = 0
        args['dtreeprune'] = True
        args['distprune'] = False
        args['d'] = True
        args['i'] = 0.75
        args['p'] = False
        args['fayyad'] = True
        esdash,totalsize,endtime,nodlea = runner(z,args,esdash,
                                  totalsize,Tname,objectives)
        self.endtime[Tname] = endtime
        ct_storeinfile(self.tname,self.gettime(Tname))

        
        
        #CT1* Fayyad on Big Tree
        Tname = 'CT1*_'+str(self.prob)+str(self.pop)
        self.starttime[Tname] = time.time()
        print ">>>>>"*10,Tname,"<<<<<"*10
        totalsize[Tname] = 0
        args['dtreeprune'] = True
        args['distprune'] = False
        args['d'] = False
        args['i'] = -1
        args['p'] = False
        args['fayyad'] = True
        esdash,totalsize,endtime,nodlea = runner(z,args,esdash,
                                  totalsize,Tname,objectives)                    
         
        self.endtime[Tname] = endtime
        ct_storeinfile(self.tname,self.gettime(Tname))
        
"""
        
