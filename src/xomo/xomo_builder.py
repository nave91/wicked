#REads in csvfile from jmoo and simulates xomo to run in MAgic

import sys,re

xomomap = {"xomofl" : "flight",
           "xomogr" : "ground",
           "xomoos" : "osp",
           "xomoo2" : "osp2",
           "xomoal" : "all"}
def line(csvfile): #returns formatted line from the csvfile 
    l = csvfile.readline()
    endcommare = re.compile('.*,$')
    if l != '':
        l = l.split('#')[0]
        l = l.replace('\t','')
        l = l.replace('\n','')
        l = l.replace('\r','')
        l = l.replace(' ','')
        endcomma = endcommare.match(l)
        if endcomma:
            ltemp = line(csvfile)
            if ltemp != -1:
                return l+ltemp
            else:
                return l
        else:
            return l
    else:
        return -1

def trials(model,pop):
    
    model = xomomap[model]
    import xomo
    c = xomo.Cocomo("../data/"+model)
    _,rows = c.trials(pop,verbose=False)
    
    #clean rows
    for _r,r in enumerate(rows):
        for _i,i in enumerate(r):
            rows[_r][_i] = round(float(i),2)
    
    return rows

def builder(csvfile):
    header = []
    rows = []
    FS = ','
    seen = False
    while True:
        lst = line(csvfile)
        if lst == -1:
            sys.stderr.write('WARNING: empty or missing file\n')
            return header,rows 
        lst = lst.split(FS)
        if lst != ['']:
            if seen:
                rows.append(lst)
            else:
                seen = True
                header = lst

def xomo_csvmaker(model,rows,verbose=False,names=None):
    if names: header = names
    else:
        header = ['?aa','$sced','$cplx','$site','$resl','$acap',
              '$etat','$rely','$data','$prec','$pmat','$aexp',
              '$flex','$pcon','$tool','$time','$stor','$docu',
              '?b','$plex','$pcap','+kloc','$ltex','$pr','$ruse',
              '$team','$pvol']
    if names: header = names
    objectives = ['-effort','-months','-defects','-risks']
    import xomo
    model = xomomap[model] if model in xomomap else model
    c = xomo.Cocomo("../data/"+str(model))
    bigrows = []
    #clean rows
    for _r,r in enumerate(rows):
        for _i,i in enumerate(r):
            rows[_r][_i] = round(float(i),2)
    headerwithoutsyms = [i[1:] for i in header]
    #simulate xomo
    for r in rows:
        vals = c.simulate(headerwithoutsyms,r)
        bigrow = r+[round(i,2) for i in vals]
        bigrows.append(bigrow)
    
    header += objectives
    
    if verbose:
        s = ''
        for i in header:
            s += str(i)+','
        print s[:len(s)-1]
        for r in bigrows:
            s = ''
            for i in r:
                s +=str(i) + ','
            print s[:len(s)-1]
    return header,bigrows



if __name__ == "__main__":

    header,rows = builder('xomofl',200)
    print header,rows[0],len(rows)
