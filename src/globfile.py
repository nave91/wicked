#
#GLOBAL CONST MODELS
#
XOMOPROB = ["xomofl","xomogr","xomoos","xomoo2","xomoal"]
POMPROB = ["pom3A","pom3B","pom3C"]
DTLZPROB = ["dtlz1","dtlz2","dtlz3","dtlz4"]
#
#Properties for table
#
name = ""
z = "main"
zout = "out"
shortz = "shortenedz"
args = {'v' : -1,                      #Verbose
        'ifile' : '',                  #input file
        'e' : 'median',                #evaluation criteria
        'p' : False,                   #Pruning
        'n' : -1,                      #nearest percentage to learn
        'spy': False,                  #print tree
        'l' : 20,                      #min samples per leaf
        'c' : 'entropy',               #criteria for CART
        'smin' : -1,                   #size of cluster min
        'smax' : -1,                   #size of cluster max
        'm' : 'flight',                #default model
        't' : 'graphed_output',        #default name of graph
        'chops' : [0.25,0.5,0.75,1],   #chops
        'out': 'effrange',             #default file name
        'jmoo':'_',                    #default jmoo file
        'dtreeprune': False,           #decision tree pruning
        'i' : 0.5,                     #percentage infogain used
        'd' : False,                   #discretization
        'distprune': False,            #distance pruning
        'bpop': 1000,                  #bootstrap population
        'fayyad': False,               #fayyad disc check
        'objind' : (-1,-1),            #num of deps and indeps for dtlz
        'repeats': 20,                 #total no of times experi is done
        'gens': 1                      #number of gens from wicked 
        }
#
#Info for table
#
csvindex = -1 #initialized to -1 as lists start at zero
colname = {k: [] for k in range(1)} #stores dict of names of columns
data = {k: [] for k in range(1)} #stores dict of list of lists containing each row
test = [] #stores test data
#
#metadata
#
order = {k:dict.fromkeys(colname) for k in range(1)} #stores colnames and index of column in csv
klass = {k: [] for k in range(1)} #dict of list of klass columns
more = {k: [] for k in range(1)} #dict of list of more columns
less = {k: [] for k in range(1)} #dict of list of less columns
num = {k: [] for k in range(1)} #dict of list of num columns
term = {k: [] for k in range(1)} #dict of list of term columns
dep = {k: [] for k in range(1)} #dict of list of dependent columns
indep = {k: [] for k in range(1)} #dict of list of independent columns
nump = {k: [] for k in range(1)} #dict of list containing nump column names
wordp = {k: [] for k in range(1)} #dict of list containing wordp column names
#
#for nump values
#
hi = {k:dict.fromkeys(nump) for k in range(1)} #dictionary containing highest values of nump columns 
lo = {k:dict.fromkeys(nump) for k in range(1)} #dictionary containing lowest values of nump columns
mu = {k:dict.fromkeys(nump) for k in range(1)} #dictionary containing mean values of nump columns
m2 = {k:dict.fromkeys(nump) for k in range(1)} #dictionary containing m2 values of nump columns
sd = {k:dict.fromkeys(nump) for k in range(1)} #dictionary containing std dev of nump columns
#
#for wordp values
#
mode = {k:dict.fromkeys(wordp) for k in range(1)} #dictionary containing mode of wordp columns
most = {k:dict.fromkeys(wordp) for k in range(1)} #dictionary containing most occured item of wordp columns
count = {k:dict(dict.fromkeys(wordp)) for k in range(1) }#dictionary of dictionaries of count of each item in each wordp column
#
#for all
#
n = {k:dict.fromkeys(colname) for k in range(1)} #stores number of elements in each column
isnum = True
#
#for the zeror
#
hypotheses = {}
#
#Number of unfilled columns
nulls= {k: {} for k in range(1)}
#
#For dependent variables the MRE values of ONE dep can be stored in 
mre = {}
#For shortened tree discretizer
buckets = {}
