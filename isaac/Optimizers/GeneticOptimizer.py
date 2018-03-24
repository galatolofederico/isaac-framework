from Optimizer import Optimizer

import random,time,sys
import threading
import numpy as np
import time, random


def th(n, max):
    return int(max) if n > max else int(n)

class Counter:
    def __init__(self, max):
        self.max = max
        self.counter = 0
        self.finished = 0
        self.lock = threading.Lock()
    
    def get(self):
        return self.counter
    
    def thereIsMore(self):
        return 1 if self.counter < self.max else 0
        
    def getAndInc(self):
        self.lock.acquire()
        if self.counter >= self.max:
            next = -1
        else:
            next = self.counter
            self.counter += 1
        self.lock.release()
        return next
    
    def signal(self):
        self.lock.acquire()
        self.finished += 1
        self.lock.release()
    
    def isFinished(self):
        return self.finished >= self.max
        
class Worker(threading.Thread):
    def __init__(self, population, counter, constraints):
        threading.Thread.__init__(self)
        self.population = population
        self.counter = counter
        self.constraints = constraints
    
    def run(self):
        while self.counter.thereIsMore():
            i = self.counter.getAndInc()
            if i == -1:
                break
            self.population[i][1] = self.population[i][0].evaluate(self.constraints)
            self.counter.signal()

class GeneticOptimizer(Optimizer):
    def __init__(self, **kargs):
        Optimizer.__init__(self, **kargs)
        self.epochs = 0
        self.npop = 10
        if "population" in kargs:
            self.npop = kargs["population"]
        self.mutationrate = 0.2
        if "mutationrate" in kargs:
            self.mutationrate = kargs["mutationrate"]
        self.threads = 4
        if "threads" in kargs:
            self.threads = kargs["threads"]

        self.population = []
        self.MAX_INT = 2**32 if not self.maximize else -2**32
        for _ in range(0,self.npop):
            self.population.append([self.getInstance(), self.MAX_INT])
        
        self.lastscore = self.MAX_INT
        
    
    def epoch(self):
        self.epochs += 1    
        counter = Counter(self.npop)
        threads = []
        for _ in range(0, self.threads):
            worker = Worker(self.population, counter, self.constraints)
            threads.append(worker)
            worker.start()
        for t in threads:
            t.join()

        self.population = sorted(self.population, key=lambda x: x[1], reverse=self.maximize)
        
        newpop = [self.population[0]]
        for _ in range(0, self.npop):
            # normal distribution with sigma=4, 70% of couples in first best 4
            # 4% to hit the same couple (0.5)**2(1-phi(1/4))**2
            # 50% to have almost one identical couple
            # (binomial experiment with p=0.04 n=20) in a 10 being population (poisson lambda=0.8)
            # to fix
            first = th(round(abs(np.random.normal(0, 4))), self.npop-1)
            second = th(round(abs(np.random.normal(0, 4))), self.npop-1)
            while first == second:
                second = th(round(abs(np.random.normal(0, 4))), self.npop-1)
            c = self.crossover(self.population[first][0], self.population[second][0])
            newpop.append([c[0], self.MAX_INT])
            newpop.append([c[1], self.MAX_INT])
        
        counter = Counter(len(newpop))
        threads = []
        for _ in range(0, self.threads):
            worker = Worker(newpop, counter, self.constraints)
            threads.append(worker)
            worker.start()

        for t in threads:
            t.join()

        newpop = sorted(newpop, key=lambda x: x[1], reverse=self.maximize)

        self.population = newpop[0:self.npop]
        self.lastscore = self.population[0][1]
        
    def crossover(self,a,b):
        a_chromosomes = a.serialize()
        b_chromosomes = b.serialize()
        
        newa = self.getInstance()
        newb = self.getInstance()
        
        new_a_chromosomes = {}
        new_b_chromosomes = {}
        
        for key in a_chromosomes:
            a_chromosome = a_chromosomes[key][:]
            b_chromosome = b_chromosomes[key][:]
            pivot = random.randint(0,len(a_chromosome))

            new_a_chromosomes[key] = a_chromosome[0:pivot] + b_chromosome[pivot:]
            new_b_chromosomes[key] = b_chromosome[0:pivot] + a_chromosome[pivot:]

        newa.deserialize(new_a_chromosomes)
        newb.deserialize(new_b_chromosomes)

        
        newa.mutation() if random.random() > self.mutationrate else 0
        newb.mutation() if random.random() > self.mutationrate else 0
         
        return [newa, newb]
    
    def hasFinished(self):
        return self.lastscore == 0

    def __str__(self):
        return "(epoch: "+str(self.epochs)+", score: "+str(self.lastscore)+")\n"
    
    def getResult(self):
        return self.population[0][0]
