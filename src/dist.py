#Module to report distances
from reader import *
sys.do_not_write_bytecode = True

def dist(this,that,z,indep,nump):
    #returns distance between this and that
    tot = 0.0
    for k in indep[z]:
        ind = colname[z].index(k)
        v1 = this[ind]
        v2 = that[ind]
        #print ">","v1",v1,"v2",v2
        if (v1 == "?" or v1 == "") and (v2 == "?" or v2 == ""):
            tot+=1
        elif k in nump[z]:
            aLittle = 0.0000001
            mid = (hi[z][k] - lo[z][k])/2
            #v1 = float(v1)
            if v1 == "?" or v1 == "":
                v1 = 1 if v2 < mid else 0
            else:
                v1 = (v1 - lo[z][k])/ (hi[z][k] - lo[z][k] + aLittle)
            if v2 == "?" or v2 == "":
                v2 = 1 if v1 < mid else 0
            else:
                v2 = (v2 - lo[z][k])/ (hi[z][k] - lo[z][k] + aLittle)
            tot += (v2-v1)**2
        else:
            if v1 == "?" or v1 == "":
                tot += 1
            elif v2 == "?" or v2 == "":
                tot += 1
            elif v1 != v2:
                tot += 1
            else:
                tot += 0
    ret = tot**0.5 / (len(indep[z]))**0.5
    return ret

def closest(i,z,selfie,data):
    #returns row in z closest to i
    mini = 0.0001
    indi = data[z].index(i)
    for j in data[z]:
        if i == j and i != selfie:
            continue
        d = dist(data[z][i],data[z][j],z,indep,nump)
        if d > maxi:
            maxi = d
            out = j
    return out

def furthest(i,data,z):
    #returns row furthest to i
    maxi = -1
    out = 0
    for j in data[z]:
        d = dist(data[z][i],j,z,indep,nump)
        if d > maxi:
            maxi = d
            out = j
    return out


if __name__ == "__main__":
    name = os.path.basename(__file__).split('.')[0]
    get_args(name,args)
    #Read csvfile
    csvfile = open('../data/'+args['ifile']+'.csv','r')
    #Main table is initialized as "main"
    z = "main"
    readCsv(csvfile,z)
    if len(args['v'])>-1:
        for i in range(0,len(data[z])):
            for j in range(0,len(data[z])):
                print dist(data[z][i],data[z][j],z,indep,nump)

