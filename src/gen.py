
#from xomod import *
from diff import *
import os

def applydiffs(c,col,m,thresh,verbose):
    k = filter(lambda x: x.txt == col,c.about())[0]
    if verbose: print k.txt,k.min,k.max,">before"
    if m == "max":
        max = thresh 
        k.update(k.min,max,m=c)
    elif m == "min":
        min = thresh
        k.update(min,k.max,m=c)
    if verbose: print k.txt, k.min, k.max,">after"

def clearsymbols(col):
    import re
    col = re.sub(r'[^\w]', '', col) 
    return col

def gen(z,
        chops,
        output=os.environ["HOME"]+"/tmp/xomo",
        data = "../data",
        model=None,
        verbose=False):
    differs = diff(z)
    c,model = xomod1()
    if verbose: print differs
    for i in differs:
        fea = i[0]
        cond = i[1]
        thresh = i[2]
        if fea not in dep[z]:
            fea = clearsymbols(fea)
            if cond:
                applydiffs(c,fea,"max",thresh,verbose)
            else:
                applydiffs(c,fea,"min",thresh,verbose)
            if verbose:
                print "Sample of 5"
                for _ in range(5):
                    print fea, c.xys()[0][fea]
    znew = 'gened'
    c.xys(verbose = False)
    out = output + "/" + model + ".csv"
    c.trials(out=out,verbose=False)
    sys.stderr.write("# see" + out + "\n")
    reader.readCsv(open(out,'r'),znew)
    dec,inc,same = depsptiles(z,znew,chops,True)
    print "decs:",dec,"incs:",inc,"sames:",same
    return depsptile(znew,chops)

def genwithdiffs(Diffs,betters,model,verbose):
    
    diffclus = betters

    if args['m'] in XOMOPROB: function = genwithdiffs_xomo
    elif args['m'] in POMPROB: function = genwithdiffs_pom
    elif args['m'] in DTLZPROB: function = genwithdiffs_dtlz
    else:
        #model not recognized
        print "!"*30,"stuck in difff","!"*30
        sys.exit()
                    
    for d in Diffs:
        diffclus.append(d.generate(function,model,verbose=False))
    return diffclus

def genwithdiffs_xomo(z,
         diffs,
         model,
         output=os.environ["HOME"]+"/tmp/xomo",
         data = "../data",
         verbose=False,write=False,n=500):
    from xomod import xomod1
    c,model = xomod1(model=model)
    for i in diffs:
        fea = i[0]
        cond = i[1]
        thresh = i[2]
        fea = clearsymbols(fea)
        if cond:
            applydiffs(c,fea,"max",thresh,verbose)
        else:
            applydiffs(c,fea,"min",thresh,verbose)
        if verbose:
            print "Sample of 5"
            print i
            for _ in range(5):
                print fea, c.xys()[0][fea]
    znew = z + 'gened'
    c.xys(verbose = False)
    out = output + "/" + str(model) + str(znew) + ".csv"
    header,rows = c.trials(n=n,out=out,verbose=False,write=write)
    reader.makeTable(header,znew)
    for i in rows:
        reader.addRow(i,znew)
    sys.stderr.write("# Table " + znew + " created\n")
    if write: sys.stderr.write("# see" + out + "\n")
    if write: reader.readCsv(open(out,'r'),znew)
    return znew

def genwithdiffs_pom(z,
         diffs,
         model,
         output=os.environ["HOME"]+"/tmp/pom",
         data = "../data",
         verbose=False,n=500):
    from pom3d import *
    os = Os(model) 
    for i in diffs:
        fea = i[0]
        cond = i[1]
        thresh = i[2]
        fea = clearsymbols(fea)
        os.update(fea,cond,thresh)
        if verbose:
            print "Sample of 5"
            print i
            os.trials(5,verbose=True)
    znew = z + 'gened'
    out = output + "/" + znew + ".csv"
    header,rows = os.trials(N=n,verbose=False)
    reader.makeTable(header,znew)
    for i in rows:
        reader.addRow(i,znew)
    sys.stderr.write("# Table " + znew + " created\n")
    return znew

def genwithdiffs_dtlz(z,
         diffs,
         model,
         output=os.environ["HOME"]+"/tmp/pom",
         data = "../data",
         verbose=False,n=500):
    from dtlzd import *
    os = Os(model,args['objind']) 
    for i in diffs:
        fea = i[0]
        cond = i[1]
        thresh = i[2]
        fea = clearsymbols(fea)
        os.update(fea,cond,thresh)
        if verbose:
            print "Sample of 5"
            print i
            os.trials(5,verbose=True)
    znew = z + 'gened'
    out = output + "/" + znew + ".csv"
    header,rows = os.trials(N=n,verbose=False)
    reader.makeTable(header,znew)
    for i in rows:
        reader.addRow(i,znew)
    sys.stderr.write("# Table " + znew + " created\n")
    return znew
       
def genwithrange(z,
                 ranges,
                 output=os.environ["HOME"]+"/tmp/xomo",
                 data = "../data",
                 model=None,
                 verbose=False):
    c,model = xomod1()
    for R in ranges:
        applydiffs(c,R.feature,"max",R.max,verbose)
        applydiffs(c,R.feature,"min",R.min,verbose)
    znew = z + 'gened'
    c.xys(verbose = False)
    out = output + "/" + model + znew + ".csv"
    c.trials(out=out,verbose=False)
    sys.stderr.write("# see" + out + "\n")
    reader.readCsv(open(out,'r'),znew)
    return znew

conv = {

'$prec' : 'prec',
'$flex' : 'flex',
'$resl' : 'resl',
'$team' : 'team',
'$pmat' : 'pmat',
'$rely' : 'rely',
'$cplx' : 'cplx',
'$data' : 'data',
'$ruse' : 'ruse',
'$time' : 'time',
'$stor' : 'stor',
'$pvol' : 'pvol',
'$acap' : 'acap',
'$pcap' : 'pcap',
'$pcon' : 'pcon',
#'$apex' : 'apex',
'$plex' : 'plex',
'$ltex' : 'ltex',
'$tool' : 'tool',
'$sced' : 'sced',
'$site' : 'site',
'$docu' : 'docu',
'-LogicalEKLOC' : 'kloc',
'$LogicalEKLOC' : 'kloc',
'$ACT_EFFORT' : '-effort',
}

        

if __name__ == "__main__":
    sys.do_not_write_bytecode = True
    name = os.path.basename(__file__).split('.')[0]
    get_args(name,args)
    #Read csvfile
    csvfile = open('../data/'+args['ifile']+'.csv','r')
    #First table is initialized with name "main"
    z = "main"
    reader.readCsv(csvfile,z)
    chops = [0.25,0.5,0.75,1.0]
    gen1(z,chops,args['m'])
