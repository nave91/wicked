import globfile as _glob
import _nave_interface as _nave
import sys
import reader

ALGOS = ["CT"]
PROBS = ["pom3B"]#["xomofl","xomogr","xomoos","xomoo2","xomoal"]#["pom3A","pom3B","pom3C"] #
POPS = [500]#[100,200,300,400,500]
INDS = [20]#[20,40,60,80]
OBJS = [2]#[2,4,8]

if len(sys.argv) > 1:
    PROBS = ["pom3A"]
    POPS = [400]

RCT = "CT/allctresults/ct_" #record final tek results
TCT = "CT/allcttimes/ct_" #record times
NLCT = "CT/allctnodleas/ct_" #record no. of nodes leaves
DCT = "CT/allctdisplays/ct_" #record all displays
PCT = "CT/allpops/pop_jmoo_" #population input
JCT = "CT/alljresults/jmoo_" #jmoo results as input
JTCT = "CT/alltimes/jmoo_" #jmoo times as input

if PROBS[0][:3] in ["pom","xom"]:
    for algo in ALGOS:
        for prob in PROBS:
            for pop in POPS:
                print "#"*25,algo,prob,pop
                sys.stderr.write("****"*20+" "+str(algo)
                                 +" "+str(prob)
                                 +" "+str(pop)
                                 +" "+"****"*20+"\n")
                rname = RCT+prob+str(pop)+".tek" 
                tname = TCT+prob+str(pop)+".time" 
                nlname = NLCT+prob+str(pop)+".count"
                dname = DCT+prob+str(pop)+".show"
                pname = PCT+prob+str(pop)+".csv"
                jname = JCT+prob+str(pop)+".pickle"
                jtname = JTCT+prob+str(pop)+".time"
                interface = _nave.Interface(algo,prob,pop,rname,
                                            pname,jname,nlname,
                                            tname,dname,jtname=jtname)
                interface.run()
                #Clean up
                for key,value in _nave.data.items():
                    reader.removeTable(key)
                _glob.buckets = {}


elif PROBS[0][:4] in ["dtlz"]:
    for algo in ALGOS:
        for prob in PROBS:
            for obj in OBJS: 
                for objind in zip([obj for i in range(len(INDS))],INDS):
                    for pop in POPS:
                        print "#"*25,algo,prob,pop
                        _o = str(objind[0])+'o_'+str(objind[1])+'i'
                        sys.stderr.write("****"*20+" "+str(algo)
                                         +" "+str(prob)
                                         +" "+str(pop)
                                         +" "+str(_o)
                                         +" "+"****"*20+"\n")
                        rname = RCT+prob+str(pop)+"_"+str(_o)+".tek" 
                        pname = PCT+prob+str(pop)+"_"+str(_o)+".csv"
                        jname = JCT+prob+str(pop)+"_"+str(_o)+".pickle"
                        nlname = NLCT+prob+str(pop)+"_"+str(_o)+".count"
                        tname = TCT+prob+str(pop)+"_"+str(_o)+".time" 
                        dname = DCT+prob+str(pop)+"_"+str(_o)+".show"
                        interface = _nave.Interface(algo,prob,pop,rname,
                                                    pname,jname,nlname,
                                                    tname,dname,objind=objind)
                        interface.run()
                        #Clean up
                        for key,value in _nave.data.items():
                            reader.removeTable(key)                       
                        _glob.buckets = {}
                

else:
    print "ERROR: GET YOUR PROBS STRAIGHT IN NAVE_INTERFACE!"
    sys.exit()
