from reader import *
from table import *
from lib import *

dense = 'dense'
sparse = 'sparse'

def calcNulls(z):
    newddict(nulls,z)
    for ind,r in enumerate(data[z]):
        temp = 0
        nulls[z][ind] = 0
        for c in colname[z]:
            cind = indexOf(z,c)
            if r[cind] == '?':
                temp += 1
        nulls[z][ind] = temp
    return nulls

def groupzNulls(z,zminusd,depp,density=0.5,usedepp=True):
    nulls = calcNulls(zminusd)
    cols = len(colname[zminusd])
    makeTable(colname[zminusd],dense)
    makeTable(colname[zminusd],sparse)
    if usedepp: effindex = indexOf(z,depp)
    for key,d in nulls[zminusd].items():
        if d  < int(cols*density):
            if usedepp:
            #Only records with depp
                if data[z][key][effindex] != '?':
                    addRow(data[zminusd][key],dense)
                else:
                    addRow(data[zminusd][key],sparse)
            else:
                addRow(data[zminusd][key],dense)
        else:
            addRow(data[zminusd][key],sparse)

def groupzNulls1(zminusd,depp,density=0.5,usedepp=True):
    z = zminusd
    nulls = calcNulls(zminusd)
    cols = len(colname[zminusd])
    makeTable(colname[zminusd],dense)
    makeTable(colname[zminusd],sparse)
    if usedepp: effindex = indexOf(z,depp)
    for key,d in nulls[zminusd].items():
        if d  < int(cols*density):
            if usedepp:
            #Only records with depp
                if data[z][key][effindex] != '?':
                    addRow(data[zminusd][key],dense)
                else:
                    addRow(data[zminusd][key],sparse)
            else:
                addRow(data[zminusd][key],dense)
        else:
            addRow(data[zminusd][key],sparse)
