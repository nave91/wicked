#REads in csvfile from jmoo and simulates pom to run in MAgic

import sys,re

    
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
    
def pom3_csvmaker(names,rows,verbose=True):
    header = names[:]
    objectives = ['-cost','+completion','-idle']
    import pom3
    p3 = pom3.pom3()
    bigrows = []
    #clean rows
    for _r,r in enumerate(rows):
        for _i,i in enumerate(r):
            rows[_r][_i] = round(float(i),2)
    #simulate pom3
    for r in rows:
        vals = p3.simulate(r)
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
    csvfile = sys.argv[1]
    csvfile = open('inp/'+str(csvfile)+'.csv','r')
    header,rows = builder(csvfile)
    pom3_csvmaker(header,rows)
    
