
#from xomod import *
from diff import *
from properties import *
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
        tmp = d.generate(function,model,verbose=False)
        if tmp: diffclus.append(tmp)
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

def smartsamples(Diffs,betters,model,verbose):

    
    #adding actual betters
    bets = 'betters'
    reader.makeTable(colname[z],bets)
    for b in betters:
        for r in data[b]:
            ind = data[shortz].index(r[:-1])
            reader.addRow(data[z][ind],bets)

    #betters to new clus
    diffclus = [bets] 
    if args['m'] in XOMOPROB: function = smartsamples_xomo
    elif args['m'] in POMPROB: function = smartsamples_pom
    elif args['m'] in DTLZPROB: function = smartsamples_dtlz
    else:
        #model not recognized
        print "!"*30,"stuck in difff","!"*30
        sys.exit()
              
    for d in Diffs:
        tmp = d.generate(function,model,verbose=False)
        if tmp: diffclus.append(tmp)
    
    if len(diffclus) == 0: 
        raise(ValueError,"Check gen!!")
        
    return diffclus


def smartsamples_pom(z,
                    diffs,
                    model,
                    n=500,
                    verbose=False):
    rows = []

    shortz,main = 'shortenedz','main'
    if len(data[z]) < 3:
        return None
    #find actual rows not shortened ones
    actualrows = []
    for r in data[z]:
        ind = data[shortz].index(r[:-1])
        actualrows.append(ind)
        
    for i in range(n):
        row = []
        #smart sample all
        R = MODEL[model]
        for fea in indep[main]:
            fi = colname[main].index(fea)
            _a,_b,_c = random.sample(actualrows,3)
            a,b,c = data[main][_a][fi],data[main][_b][fi],\
                    data[main][_c][fi]
            if b == c: new = b
            else:                
                new = a + random.uniform(b,c)
                if new > R['UPS'][fi]:
                    new = R['LOWS'][fi] + (new - R['UPS'][fi])
                    # sanity check
                    if new > R['UPS'][fi]:
                        new = R['LOWS'][fi] + (new - R['UPS'][fi])
            row.append(round(new,2))
        # modify fea values in diffs
        for i in diffs:
            fea = i[0]
            cond = i[1]
            thresh = i[2]
            fi = colname[main].index(fea)
            if cond:
                val = random.uniform(R['LOWS'][fi],thresh)
            else:
                val = random.uniform(thresh,R['UPS'][fi])
            row[fi] = round(val,2)
        rows.append(row)
    znew = z + 'gened'
    #manage header
    header = indep[main]
    from pom3d import *
    header,rows = pomrunner(header,rows,verbose=False)
    reader.makeTable(header,znew)
    for i in rows: reader.addRow(i,znew)
    sys.stderr.write("# Table " + znew + " created.\n")
    return znew
    

def smartsamples_xomo(z,
                      diffs,
                      model,
                      n=500,
                      verbose=False):
    rows = []
    shortz,main = 'shortenedz','main'
    if len(data[z]) < 3:
        return None
    
    actualrows = []
    for r in data[z]:
        ind = data[shortz].index(r[:-1])
        actualrows.append(ind)
    
    R = ()
    def fearange(fea):
        if fea in MODEL[model]:
            R = MODEL[model][fea]
        else:
            R = MODEL["xomogeneric"][fea]
        return R
    
    for i in range(n*100):
        row = []
        #smart sample all
        for fea in indep[main]+['+kloc']:
            fi = colname[main].index(fea)
            _a,_b,_c = random.sample(actualrows,3)
            a,b,c = data[main][_a][fi],data[main][_b][fi],\
                    data[main][_c][fi]
            if b == c: new = b
            else:                
                new = a + random.uniform(b,c)
                R = fearange(fea[1:])
                if new > max(R):
                    new = min(R) + (new - max(R))
                    #sanity check
                    if new > max(R):
                        new = min(R) + (new - max(R))
            row.append(round(new,2))
        for i in diffs:
            fea = i[0]
            cond = i[1]
            thresh = i[2]
            R = fearange(fea[1:])
            if cond:
                val = random.uniform(min(R),thresh)
            else:
                val = random.uniform(thresh,max(R))
            fi = colname[z].index(fea)
            row[fi] = round(val,2)
        rows.append(row)

    from xomo import xomo_builder
    znew = z + 'gened'
    header = indep[main]+['+kloc']
    header,rows = xomo_builder.xomo_csvmaker(args['m'],rows,names=header)
    reader.makeTable(header,znew)
    for i in rows: reader.addRow(i,znew)
    sys.stderr.write("# Table "+ znew + "created.\n")
    return znew

def smartsamples_dtlz(z,
                      diffs,
                      model,
                      n=500,
                      verbose=False):
    rows = []
    shortz,main = 'shortenedz','main'
    if len(data[z]) < 3:
        return None
    #find actual rows not shortened ones
    actualrows = []
    for r in data[z]:
        ind = data[shortz].index(r[:-1])
        actualrows.append(ind)
        
    for i in range(n):
        row = []
        #smart sample all
        R = MODEL[model[:-1]]
        for fea in indep[main]:
            fi = colname[main].index(fea)
            _a,_b,_c = random.sample(actualrows,3)
            a,b,c = data[main][_a][fi],data[main][_b][fi],\
                    data[main][_c][fi]
            if b == c: new = b
            else:                
                new = a + random.uniform(b,c)
                if new > max(R):
                    new = min(R) + (new - max(R))
                    #sanity check
                    if new > max(R):
                        new = min(R) + (new - max(R))
            row.append(round(new,2))
        for i in diffs:
            fea = i[0]
            cond = i[1]
            thresh = i[2]
            R = MODEL[model[:-1]]
            if cond:
                val = random.uniform(min(R),thresh)
            else:
                val = random.uniform(thresh,max(R))
            fi = colname[z].index(fea)
            row[fi] = round(val,2)
        rows.append(row)

    from dtlzd import Os
    znew = z + 'gened'
    header = indep[main]
    next_dtlz = Os(args['m'],args['objind'])
    rows = next_dtlz.runner(rows)
    reader.makeTable(colname[main],znew)
    for r in rows: reader.addRow(r,znew)
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
    import reader
    reader.pomreadFromCT()
    smartsample_pom(z,[],'pom3A')
