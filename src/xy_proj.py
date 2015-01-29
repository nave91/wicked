#Module for spectrally clustering data from z and returning zlst
#zlst[0] is table with centroids of leaves zlst[1]..zlst[n]

#from reader import *
import xy
import re
from globfile import *
from dist import *
from table import *
from xy_lib import *

def xy_proj(z,data,args,check=False):
    e = args['e']
    leaves = {} #dict of leaves with values as list of rows
    #Round off all the  values of z to 2 decimal places
    #roundoffz(z)
    
    #Create and instantiate xy object
    z_xy = 'xy'
    xyobj = xy.xy(z_xy,'',colname[z])
    rows = xycalc(z)
    l = 0

    rows = sorted(rows)
    
    for r in rows:
        xyobj.keep(r)
        l += 1
    if args['smin'] < 0 and  args['smax'] <0: 
        l = l**0.5
        maxi = l+l
        mini = l
    else:
        maxi = args['smax']
        mini = args['smin']
    leafs = []
    #Build leaves dict from the spectral clustered data of xyobject
    for n,leaf in enumerate(xyobj.tiles(maxi,mini,0,args['spy'],
                                        args['p'],args['v'])):
        if len(leaf) > 0 and leaf not in leafs: 
            leafs.append(leaf)
    for n,leaf in enumerate(leafs):
        leaves[n] = leaf
    
    #Build a summary leaf table
    #ltab = leaftab(leaves)
    """
    #Checks for debugging
    if check == True: leafprint(leaves)
    if check == True: printltab(ltab)
    if check  == True: checkie(leaves,ltab,data)
    """
    
    #Build a z list of tables of all leaves
    zlst = makeleaftab(leaves,z)
    #build zlst[0] with centroids of all zlst[1..len]
    zlst = buildzero(zlst) 
    
    check_zlst = False #Make this True to view tabled zlst 
    if check_zlst == True:
        for i,j in enumerate(zlst):
            print ">"+str(i)
            outCsv([j])

    #new_appender = ''
    #zlst = reorder(z,zlst,appender,new_appender,e)

    #Use only n nearest elements to centroid
    if args['n'] > -1:
        zlst = nearestn(zlst,args['n'])
    if args['p']:
        tot = 0
        for i in zlst[1:]:
            tot += len(data[i])
        print "rows after pruned",tot
    
    return zlst
        

if __name__ == "__main__":
    sys.do_not_write_bytecode = True
    name = os.path.basename(__file__).split('.')[0]
    get_args(name,args)
    #Read csvfile
    csvfile = open('../data/'+args['ifile']+'.csv','r')
    #First table is initialized with name "main"
    z = "main"
    readCsv(csvfile,z)
    zlst = xy_proj(z,data,args)
    zlst = xy_proj(z,data,args)
    


    sys.exit()
    zminusd = "both-depz"
    #Remove all dependents 
    #and build new table
    coltemp = []
    for c in colname[z]:
        if c not in dep[z]:
            coltemp.append(c)
    makeTable(coltemp,zminusd)
    depind = []
    for de in dep[z]:
        depind.append(indexOf(z,de))
    for d in data[z]:
        itemtemp = []
        for inditem,item in enumerate(d):
            if inditem not in depind:
                itemtemp.append(item)
        addRow(itemtemp,zminusd)

    #zlst = xy_proj(zminusd,data,args)
    for Z in zlst[1:]:
        tempdata = []
        for ind,d in enumerate(data[Z]):
            tempdata.append(data[z][data[zminusd].index(d[:len(d)-1])]+[d[len(d)-1]])
        removeTable(Z)
        makeTable(colname[z]+['C_id'],Z)
        for d in tempdata:
            addRow(d,Z)

    removeTable(zlst[0])
    zlst = buildzero(zlst,'',args['e'])
    #import tshortener
    #tshortener.distance_pruner(zlst)
    
    if args['v']>-1:
        clusters = zlst
        #outCsv([clusters[0]])
        outCsv(clusters[1:])


###########--EXTRAS--###############
"""
    only_indeps =False
    if only_indeps:
        col_temp = []
        data_temp = []
        for C in colname[zlst[0]]:
            if C in nump[z]:
                col_temp += [C+'_lo',C,C+'_hi']
            else:
                col_temp.append(C)
        for r_ind,r in enumerate(data[zlst[0]]):
            r_temp = []
            for i_ind,item in enumerate(r):
                Z = zlst[r_ind+1]
                C = colname[Z][i_ind]
                if C in nump[Z]: 
                    if lo[Z][C] > 10000: 
                        lo_temp = -1
                    else:
                        lo_temp = lo[Z][C]
                    if hi[Z][C] < 0:
                        hi_temp = -1
                    else:
                        hi_temp = hi[Z][C]
                    r_temp += [lo_temp,item,hi_temp]
                else:
                    r_temp.append(item)
            data_temp.append(r_temp)
        makeTable(col_temp,'indeps')
        for r in data_temp:
            addRow(r,'indeps')
        outCsv(['indeps'])
"""
