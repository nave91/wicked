#Module to read csv file into tabled structure
import os
import re
import sys
from globfile import *
from table import tableprint,outCsv
from lib import *
from properties import *
sys.do_not_write_bytecode = True

def makeTable(lst,z):
    #Makes table with columns lst and name z
    _dlsts = [klass,less,more,num,term,dep,
            indep,nump,wordp,colname,data]
    _ddicts = [order,count,n,mode,most,hi,lo,
             mu,m2,sd,mre]
    for _i in _dlsts: newdlist(_i,z)
    for _i in _ddicts: newddict(_i,z)
    csvindex = -1
    for csvcol in lst:
        isnum=True
        csvindex+=1
        ignore = re.match('\?.*$',csvcol)
        if ignore:
            continue
        else:
            colname[z].append(csvcol)
            order[z][csvcol] = csvindex
            klasschk = re.match('!.*$',csvcol)
            klasschk1 = re.match('=.*$',csvcol)
            klasschk2 = re.match('<.*$',csvcol)
            morechk = re.match('\+.*$',csvcol)
            lesschk = re.match('-.*$',csvcol)
            numchk = re.match('\$.*$',csvcol)
            if klasschk or klasschk1 or klasschk2:
                dep[z].append(csvcol)
                klass[z].append(csvcol)
                isnum = False
            elif morechk:
                dep[z].append(csvcol)
                more[z].append(csvcol)
            elif lesschk:
                dep[z].append(csvcol)
                less[z].append(csvcol)
            elif numchk:
                indep[z].append(csvcol)
                num[z].append(csvcol)
            else:
                indep[z].append(csvcol)
                term[z].append(csvcol)
                isnum = False
            n[z][csvcol] = 0
            if isnum:
                nump[z].append(csvcol)
                hi[z][csvcol] = 0.1 * (-10**13)
                lo[z][csvcol] = 0.1 * (10**13)
                mu[z][csvcol] = 0.0
                m2[z][csvcol] = 0.0
                sd[z][csvcol] = 0.0
            else:
                wordp[z].append(csvcol)
                count[z][csvcol] = {}
                mode[z][csvcol] = 0
                most[z][csvcol] = 0 
    
def addRow(lst,z):
    #Adds row lst to table z
    temp = []
    skip = False
    undscorechk = re.match('__.*$',str(z))
    for c in klass[z]:
        csvindex = order[z][c]
        item = lst[csvindex]
        if item != z:
            skip = True
        if z == "main" or z == "train" or undscorechk:
            skip = False
    for c in colname[z]:
        csvindex = order[z][c]
        item = lst[csvindex]
        uncertainques = re.match('\?',str(item))
        uncertainnull = re.match('^$',str(item))        
        if skip:
            return
        if uncertainques or uncertainnull:
            temp.append('?')
        else:
            n[z][c] += 1
            if c in wordp[z]:
                temp.append(item)
                try:
                    new = count[z][c][item] = count[z][c][item] + 1
                    if new > most[z][c]:
                        most[z][c] = new
                        mode[z][c] = item
                except KeyError:
                    count[z][c][item] = 1
                    if count[z][c][item] > most[z][c]: 
                        most[z][c] = 1
                        mode[z][c] = item
            else:
                item = float(item)
                temp.append(item)
                if item > hi[z][c]:
                    hi[z][c] = item
                if item < lo[z][c]:
                    lo[z][c] = item
                delta = item - mu[z][c]
                mu[z][c] += delta / n[z][c]
                m2[z][c] += delta * (item - mu[z][c])
                if n[z][c] > 1:
                    sd[z][c] = (m2[z][c] / (n[z][c] - 1))**0.5
    data[z].append(temp)
    

def readCsv(csvfile,z):
    #Reads csvfile into table z
    #resetSeed(1)
    seen = False
    FS = ','
    while True:
        lst = line(csvfile)
        if lst == -1:
            sys.stderr.write('WARNING: empty or missing file\n')
            return -1 
        lst = lst.split(FS)
        if lst != ['']:
            if seen:
                addRow(lst,z)
            else:
                seen = True
                makeTable(lst,z)

def remakeTable(z):
    temp_data = data[z][:]
    temp_col = colname[z][:]
    removeTable(z)
    makeTable(temp_col,z)
    for d in temp_data:
        addRow(d,z)

def removeTable(z):
    #Removes table and data of z
    if z in colname: del colname[z]
    if z in data: del data[z]
    if z in order: del order[z]
    if z in klass: del klass[z]
    if z in more: del more[z]
    if z in less: del less[z]
    if z in num: del num[z]
    if z in term: del term[z]
    if z in dep: del dep[z]
    if z in indep: del indep[z]
    if z in nump: del nump[z]
    if z in wordp: del wordp[z]
    if z in hi: del hi[z]
    if z in lo: del lo[z]
    if z in mu: del mu[z]
    if z in m2: del m2[z]
    if z in sd: del sd[z]
    if z in mode: del mode[z]
    if z in most: del most[z]
    if z in count: del count[z]
    if z in n: del n[z]
    from globfile import buckets
    buckets = {}

def removeData(z):
    #Removes data of z
    col = colname[z]
    removeTable(z)
    makeTable(col,z)


def copyTable(z,m,verbose):
    #copies table of z to m
    makeTable(colname[z],m)
    for r in data[z]:
        addRow(r,m)
    if verbose > 0:
        print "# copied z to m"
        print len(data[z]),len(data[m])
        print colname[m]

def xomoreadFromCT():
    #Read csvfile
    csvfile = open(args['ifile'],'r')
    from xomo import xomo_builder
    header,rows = xomo_builder.builder(csvfile)
    #Use header[:-4] to avoid extra column names in input from jmoo
    header,rows = xomo_builder.xomo_csvmaker('xomofl',rows,
                                             verbose=False)
    
    makeTable(header,z)
    for r in rows: addRow(r,z)
    
    csvfile.close()
    return header,rows

def pomreadFromCT():
    csvfile = open(args['ifile'],'r')
    from pom3 import pom3_builder
    header,rows = pom3_builder.builder(csvfile)
    #Use header[:-4] to avoid extra column names in input from jmoo
    header,rows = pom3_builder.pom3_csvmaker(header[:-4],rows,
                                             verbose=False)
    makeTable(header,z)
    for r in rows: addRow(r,z)
    csvfile.close()
    return header,rows


if __name__ == "__main__":

    name = os.path.basename(__file__).split('.')[0]
    get_args(name,args)

    header,rows = readFromCT()
    print header
    if args['v']>-1:
        outCsv([z])
    if args['v']>0:
        tableprint(z,args['e'])
