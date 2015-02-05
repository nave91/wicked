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
        'repeats': 1,                 #total no of times experi is done
        'gens': 5                      #number of gens from wicked 
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

#Model ranges
MODEL = { 
          "dtlz": (0,1),

          "pom3A": 
          {
              "LOWS" : [0.1, 0.82, 2,  0.40, 1,   1,  0, 0, 1],
              "UPS"  : [0.9, 1.20, 10, 0.70, 100, 50, 4, 5, 44]
              },
          "pom3B":
          {
              "LOWS" : [0.10, 0.82, 80, 0.40, 0,   1, 0, 0, 1],
              "UPS"  : [0.90, 1.26, 95, 0.70, 100, 50, 2, 5, 20]
          },
          "pom3C":
          {
              "LOWS" : [0.50, 0.82, 2, 0.20, 0,  40, 2, 0, 20],
              "UPS"  : [0.90, 1.26, 8, 0.50, 50, 50, 4, 5, 44]
          },

          "xomogeneric": 
          {     "aa" : (1,6),
                "sced" : (1.00,1.43), 
                "cplx" : (0.73,1.74),
                "site" : (0.80, 1.22),
                "resl" : (1.41,7.07),
                "acap" : (0.71,1.42),
                "etat" : (1,6),
                "rely" : (0.82,1.26),
                "data" : (0.90,1.28),
                "prec" : (1.24,6.20),
                "pmat" : (1.56,7.80),
                "aexp" : (0.81,1.22),
                "flex" : (1.01,5.07),
                "pcon" : (0.81,1.29),
                "tool" : (0.78,1.17),
                "time" : (1.00,1.63),
                "stor" : (1.00,1.46),
                "docu" : (0.81,1.23), 
                "b" : (3,10),
                "plex" : (0.85,1.19),
                "pcap" : (0.76,1.34),
                "kloc" : (2,1000),
                "ltex" : (0.84,1.20),
                "pr" : (1,6), 
                "ruse" : (0.95,1.24), 
                "team" : (1.01,5.48), 
                "pvol" : (0.87,1.30)
            }, 
          "xomofl": 
          {     "prec" : (6.2,1.24),
                "flex" : (5.07,1.01),
                "resl" : (7.07,1.41),
                "team" : (5.48,1.01),
                "pmat" : (6.24,4.68),
                "rely" : (1,1.26),
                "cplx" : (1,1.74),
                "data" : (0.9,1),
                "ruse" : (0.95,1.24),
                "time" : (1,1.11),
                "stor" : (1,1.05),
                "pvol" : (0.87,1.3),
                "acap" : (1,0.71),
                "pcap" : (1,0.76),
                "pcon" : (1.29,0.81),
                "aexp" : (1.22,0.81),
                "plex" : (1.19,0.91),
                "ltex" : (1.2,0.91),
                "tool" : (1.09,1.09),
                "sced" : (1,1),
                "site" : (1.22,0.8),
                "docu" : (0.81,1.23)
            },
          "xomogr":
          {     "prec" : (1.24,6.2),
                "flex" : (1.01,5.07),
                "resl" : (1.41,7.07),
                "team" : (1.01,5.48),
                "pmat" : (1.56,7.8),
                "rely" : (0.82,1.1),
                "cplx" : (0.73,1.17),
                "data" : (0.9,1),
                "ruse" : (0.95,1.24),
                "time" : (1,1.11),
                "stor" : (1,1.05),
                "pvol" : (0.87,1.3),
                "acap" : (0.71,1),
                "pcap" : (0.76,1),
                "pcon" : (0.81,1.29),
                "aexp" : (0.81,1.1),
                "plex" : (0.91,1.19),
                "ltex" : (0.91,1.2),
                "tool" : (1.09,1.09),
                "sced" : (1,1.43),
                "site" : (0.8,1.22),
                "docu" : (0.81,1.23),
                "kloc" : (11,392)
            },
          "xomoos":
          {     "prec" : (4.96,6.2),
                "flex" : (1.01,4.05),
                "resl" : (4.24,7.07),
                "team" : (3.29,4.38),
                "pmat" : (3.12,7.8),
                "rely" : (1.26,1.26),
                "cplx" : (1.34,1.74),
                "data" : (1,1),
                "ruse" : (0.95,1.07),
                "time" : (1,1.63),
                "stor" : (1,1.17),
                "pvol" : (0.87,0.87),
                "acap" : (1,1.19),
                "pcap" : (1,1),
                "pcon" : (1,1.12),
                "aexp" : (1,1.1),
                "plex" : (1,1),
                "ltex" : (0.91,1.09),
                "tool" : (1,1.09),
                "sced" : (1,1.43),
                "site" : (1,1),
                "docu" : (0.91,1.11),
                "kloc" : (75,125)
            },
          "xomoo2":
          {     "prec" : (1.24,3.72),
                "flex" : (3.04,3.04),
                "resl" : (2.83,2.83),
                "team" : (3.29,3.29),
                "pmat" : (1.56,3.12),
                "rely" : (1.26,1.26),
                "cplx" : (1.34,1.74),
                "data" : (1.14,1.14),
                "ruse" : (0.95,1.07),
                "time" : (1,1),
                "stor" : (1,1),
                "pvol" : (1,1),
                "acap" : (0.85,1.19),
                "pcap" : (1,1),
                "pcon" : (1,1.12),
                "aexp" : (0.88,1.1),
                "plex" : (0.91,1),
                "ltex" : (0.84,1.09),
                "tool" : (0.78,1.09),
                "sced" : (1,1.14),
                "site" : (0.8,1),
                "docu" : (1,1.11),
                "kloc" : (75,125)
            },
          "xomoal":
          {     "prec" : (1.24,6.2),
                "flex" : (1.01,5.07),
                "resl" : (1.41,7.07),
                "team" : (1.01,5.48),
                "pmat" : (1.56,7.8),
                "rely" : (0.82,1.26),
                "cplx" : (0.73,1.74),
                "data" : (0.9,1.14),
                "ruse" : (0.95,1.24),
                "time" : (1,1.63),
                "stor" : (1,1.17),
                "pvol" : (0.87,1.3),
                "acap" : (0.71,1.19),
                "pcap" : (0.76,1),
                "pcon" : (0.81,1.29),
                "aexp" : (0.81,1.22),
                "plex" : (0.91,1.19),
                "ltex" : (0.84,1.2),
                "tool" : (0.78,1.09),
                "sced" : (1,1.43),
                "site" : (0.8,1.22),
                "docu" : (0.81,1.23),
                "kloc" : (7,418)
            }
      }
