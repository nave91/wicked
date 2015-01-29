#library for xy_*.py

from reader import *
from dist import *
from sys import *
from table import *
import xy
import copy
import numpy as np

C_id='C_id'

def makeleaftab(leaves,z):
    #builds zlist from leaves
    zlst = [None]
    colname_temp = []
    row_temp = []
    colname_temp[:] = colname[z]
    colname_temp.append(C_id)
    for key,leaf in leaves.items():
        zindex = key+1
        _z = "__"+str(zindex)
        makeTable(colname_temp,_z)
        for i in leaf:
            row_temp[:] = i.row
            row_temp.append(zindex)
            addRow(row_temp,_z)
        zlst.append(_z)
    return zlst

def buildzero(zlst):
    z0 = "__0"
    zlst[0] = z0
    makeTable(colname[zlst[1]],z0)
    #Creating summaries of 1..len(zlst) into zlst[0]
    for i in range(1,len(zlst)):
        addRow(expected1(zlst[i]),z0)
    return zlst

def regroup(zlst,out):
    data_temp = []
    target_temp = []
    cindex = indexOf(zlst[1],C_id)#index of cluster id
    depindex = []
    for d in dep[zlst[0]]:
        depindex.append(indexOf(zlst[0],d))
    for i in range(1,len(zlst)):
        for row in data[zlst[i]]:
            row_temp = []
            for key,item in enumerate(row):
                if key != cindex:
                    if key not in depindex:
                        row_temp.append(item)
            data_temp.append(row_temp)
            target_temp.append(row[cindex])
    if out == "data": return data_temp
    elif out == "target": return target_temp
    else:
        print "Error: Regroup: None"
        return None

def lextract(zlst):
    z = zlst[0] #summary
    fea_ext = ['-effort','-defects','-months','-risks'] #List of features to be extracted
    out = {}
    for fea in fea_ext:
        out[fea] = []
    for row in data[z]:
        for fea in fea_ext:
            i_fea = indexOf(z,fea)
            out[fea].append(row[i_fea])
    return out


def roundoffz(z):
    for row in range(0,len(data[z])):
        for item in range(0,len(data[z][row])):
            data[z][row][item] = int(data[z][row][item])

def xycalc(z):

    rows = []
    bigger = 1.05
    some = 0.00001
    
    #Pick any row d
    d = anyi(data[z])
    if d == len(data[z]):
        d -= 1

    #Initialize x and y lists
    x = [0]*len(data[z])
    y = [0]*len(data[z])
    
    #find furthest from d
    east = furthest(d,data,z)
    west = furthest(data[z].index(east),data,z)
    inde = data[z].index(east)
    indw = data[z].index(west)
    c = dist(data[z][inde],data[z][indw],z,indep,nump)
    
    for d in data[z]:
        ind = data[z].index(d)
        a = dist(data[z][ind],data[z][inde],z,indep,nump)
        b = dist(data[z][ind],data[z][indw],z,indep,nump)
        x[ind] = (a**2 + c**2 -b**2) / (2**c + some)
        y[ind] = (a**2 - x[ind]**2)**0.5
        r = xy.row(d)
        r.x = x[ind]
        r.y = y[ind]
        #print r.x,r.y,a,b,c,data[z][ind],data[z][inde]
        rows.append(r)
        
    return rows
        
def eucldist(r1,r2,rows):
    #returns eucledian distance of(rows[r1],rows[r2])
    x = (rows[r1].x - rows[r2].x)**2
    y = (rows[r1].y - rows[r2].y)**2
    return (x + y)**0.5

def nearestrow(r,rows):
    #Find nearest row to r
    ind = -1
    for _ind,row in enumerate(rows):
        if r.row == row.row:
            ind = _ind
    if ind == -1:
        print "check nearest row in xy_lib. something went wrong."
        sys.exit()
    #ind = rows.index(r)
    dist = [-1]*len(rows)
    for row in range(0,len(rows)):
        dist[row] = eucldist(ind,row,rows)

    #maintain an original distance list
    org_dist = copy.copy(dist)
    #pop the distance from row to itself
    dist.pop(dist.index(0.0))

    if dist:
        if min(dist) == 0.0: 
            return rows[org_dist.index(min(dist))+1]
        return rows[org_dist.index(min(dist))]
    else:
        return rows[0]

def zeroofrows(rows):
    #return rows[r] that has (r.x,r.y) as (0,0)
    for r in rows:
        if r.x == 0.0:
            if r.y == 0.0:
                return rows.index(r)
    
def sortzlstbynearest(zlst,appender):
    #Calculate x,y coordinates for centroids
    rows = xycalc(zlst[0])

    #Maintain an original rows as we pop out rows
    org_rows = copy.copy(rows)
    new_zlst = []
    #find zero and append it to new_zlst
    zero = zeroofrows(rows)
    new_zlst.append("__"+appender+str(zero+1))
    near = nearestrow(rows[zero],rows)
    rows.pop(zero)
    
    while rows:
        #append the nearest row of past row to new_zlst
        new_zlst.append("__"+appender+str(org_rows.index(near)+1))
        oldnear = near
        near = nearestrow(oldnear,rows)
        rows.pop(rows.index(oldnear))

    return new_zlst

def reorder(z,zlst,appender,new_appender,e):
    #Returns new_zlst sorted according to distance to (0,0)
    new_zlst = sortzlstbynearest(zlst,appender)
    temp_zlst = copy.copy(zlst)
    zlst = [-1]*(len(new_zlst)+1)

    for index,value in enumerate(new_zlst):
        new_key = "__"+new_appender+str(index+1)
        makeTable(colname[value],new_key)
        indofC_id = indexOf(new_key,C_id)
        for row in data[value]:
            row[indofC_id] = index+1
            addRow(row,new_key)
        zlst[index+1] = new_key    
    zlst = buildzero(zlst,new_appender,e)
    for Z in temp_zlst: removeTable(Z)
    return zlst

def nearestn(zlst,near):
    #Returns zlst containing only nearest n elements to centroid
    for i in range(1,len(zlst)):
        Z = zlst[i]
        l = len(data[Z])
        dists = []
        for j in range(0,l):
            dists.append(dist(expected1(Z),data[Z][j],Z,indep,nump))
        k = 0
        #Create temporary data structure
        temp_data = [] 
        for d in sorted(dists):
            if k<= (near*l):
                r = dists.index(d)
                temp_data.append(data[Z][r])
                k += 1
            else:
                break
        
        #Remove old data and add new data
        removeData(Z)
        for r in temp_data:
            addRow(r,Z)

    return zlst

def yield_out_list(l):
    if isinstance(l,list):
        if not isinstance(l[0],list):
            return l
        else:
            return yield_out_list(l[0])

def conv_to_clus(value):
    temp = np.where(value==max(value))[0].tolist()
    temp = ['__'+str(i+1) for i in temp]
    return temp        

"""
#==========EXTRAS===========
def leafprint(leaves):
    for key,leaf in leaves.items():
        print ""
        print key
        for i in leaf:
            stri = ''
            for j in i.row:
                stri +=str(j)+","
            print "\t\t"+stri

def leaftab(leaves):
    #forms leaves from xy.py -Spectrally clustered data
    ltab = {} #ltab is summary of leaf tables with each leaf in ltab[0]..ltab[n]
    for key,leaf in leaves.items():
        ltab[key] = [0,0] #ltab[key][0] = xmu's [1]=ymu's
        ilen = 0 #number of rows
        for i in leaf:
            ltab[key][0]+=i.x
            ltab[key][1]+=i.y
            ilen+=1
        ltab[key][0] = ltab[key][0]/ilen
        ltab[key][1] = ltab[key][1]/ilen
    return ltab

def printltab(ltab):
    print "leaf tables mean x and y"
    for key,leaf in ltab.items():
        print key,leaf[0],leaf[1]

def hypbuild(data,z):
    hypotheses = {}
    for d in data[z]:
        temp = klass1(d, z)
        try:
            hypotheses[temp] += 1
            if hypotheses[temp] == 1:
                makeTable(colname[z],temp)
            addRow(d,temp)
        except KeyError:
            hypotheses[temp] = 1
            if hypotheses[temp] == 1:
                makeTable(colname[z],temp)
            addRow(d,temp)
    return hypotheses

def nearleaf(ltab,xyobj):
    #print "distances from test row to leaves"
    small = 10**23
    smallind = 0
    for key,leaf in ltab.items():
        tmp = eucldist(leaf,xyobj)
        #print key,tmp
        if tmp < small:
            small = tmp
            smallind = key
    return smallind
        
def out_reduced(leaves,close):
    tmp = []
    for i in leaves[close]:
        tmp.append(i.row)
    return tmp
   
def checkie(leaves,ltab,close,data,tz,t):
    #printltab(ltab)
    #leafprint(leaves)
    print ">>close",close
    print "+test:",data[tz][t]
    print "closest leaf:",close,":",out_reduced(leaves,close),"len:",len(leaves[close])

"""    
