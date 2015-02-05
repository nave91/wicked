
import sys
import array
import random
import json

import numpy

from math import sqrt

from deap import algorithms
from deap import base
from deap import benchmarks
from deap.benchmarks.tools import diversity, convergence, hypervolume
from deap import creator
from deap import tools



class Moea:
    def __init__(self,indeps,deps,pop=100,name='nsga'):

        self.MAXGEN = 5
        self.MU = pop
        self.CXPB = 0.9

        self.low = 0.0
        self.hi = 1.0
        self.indeps = indeps
        self.deps = deps

        self.toolbox = base.Toolbox()
        self.stats = tools.Statistics(lambda ind: ind.fitness.values)

        if name == 'nsga':
            self.initNSGAII()
        else:
            print "Give a real moea!\n Check moea.py."


    def initNSGAII(self):

        creator.create("FitnessMin", base.Fitness, weights=tuple([-1]*self.deps))
        creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMin)

        self.toolbox = base.Toolbox()

        self.toolbox.register("evaluate", benchmarks.dtlz1)
        self.toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=self.low, up=self.hi, eta=20.0)
        self.toolbox.register("mutate", tools.mutPolynomialBounded, low=self.low, up=self.hi, eta=20.0, indpb=1.0/self.indeps)
        self.toolbox.register("select", tools.selNSGA2)

    def loadPopulation(self,Pop=None):
        def uniform(low, up, size=None):
            try:
                return [random.uniform(a, b) for a, b in zip(low, up)]
            except TypeError:
                return [random.uniform(a, b) for a, b in zip([low] * size, [up] * size)]
        
        pop = []
        if Pop:
            for i in Pop:
                p = creator.Individual()
                p.fromlist(i)
                pop.append(p)
        else:
            for _ in range(self.MU):
                p = creator.Individual()
                i = uniform(self.low,self.hi,self.indeps)
                p.fromlist(i)
                pop.append(p)

        return pop


    def bstop(self,logbook,lives):
        if len(logbook) < lives:
            return False
        else:
            _l = 1
            while _l < lives:
                #_l is index from last of logbook
                #if any of objectives are increasing
                if any([i>j for i,j in zip(logbook[-_l]['med'],logbook[-_l-1]['med'])]):
                    return False
                else:
                    _l += 1
            return True
                

    def runNSGAII(self,pop,seed=None):
        random.seed(seed)


        self.stats.register("med", numpy.median, axis=0)
        self.stats.register("std", numpy.std, axis=0)
        self.stats.register("min", numpy.min, axis=0)
        self.stats.register("max", numpy.max, axis=0)
    
        logbook = tools.Logbook()
        logbook.header = "gen", "evals", "std", "min", "avg", "max"
    
        #pop = self.toolbox.population(n=self.MU)
        
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in pop if not ind.fitness.valid]
        fitnesses = []
        for inv_ind in invalid_ind:
            fitnesses.append(self.toolbox.evaluate(inv_ind,self.deps))
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # This is just to assign the crowding distance 
        # to the individuals no actual selection is done
        pop = self.toolbox.select(pop, len(pop))
        
        record = self.stats.compile(pop)
        logbook.record(gen=0, evals=len(invalid_ind), **record)

        gen,stop = 1,False
        # Begin the generational process
        while (gen < self.MAXGEN):# and not stop:
            # Vary the population
            offspring = tools.selTournamentDCD(pop, len(pop))
            offspring = [self.toolbox.clone(ind) for ind in offspring]
        
            for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
                if random.random() <= self.CXPB:
                    self.toolbox.mate(ind1, ind2)
            
                self.toolbox.mutate(ind1)
                self.toolbox.mutate(ind2)
                del ind1.fitness.values, ind2.fitness.values
        
            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = []
            for inv_ind in invalid_ind:
                fitnesses.append(self.toolbox.evaluate(inv_ind,self.deps))
            
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # Select the next generation population
            pop = self.toolbox.select(pop + offspring, self.MU)
            record = self.stats.compile(pop)
            logbook.record(gen=gen, evals=len(invalid_ind), **record)
            stop = self.bstop(logbook,2)
            gen += 1
        print gen
        return pop, logbook
        
if __name__ == "__main__":
    """
    with open("dtlz1_front.json") as optimal_front_data:
        optimal_front = json.load(optimal_front_data)
    # Use 500 of the 1000 points in the json file
    optimal_front = sorted(optimal_front[i] for i in range(0, len(optimal_front), 2))
    """
    moea = Moea(indeps=20,deps=2)
    pop = moea.loadPopulation()
    pop, stats = moea.runNSGAII(pop)
    pop.sort(key=lambda x: x.fitness.values)
    
    print(stats)
    print("Convergence: ", convergence(pop, optimal_front))
    print("Diversity: ", diversity(pop, optimal_front[0], optimal_front[-1]))
    
    import matplotlib.pyplot as plt
    import numpy
    
    front = numpy.array([ind.fitness.values for ind in pop])
    optimal_front = numpy.array(optimal_front)
    plt.scatter(optimal_front[:,0], optimal_front[:,1], c="r")
    plt.scatter(front[:,0], front[:,1], c="b")
    plt.axis("tight")
    plt.show()
