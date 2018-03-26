#! /usr/bin/env python

from __future__ import print_function
from isaac import *
import random

class Item:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight
    
    def __str__(self):
        return "(value: "+str(self.value)+", weight: "+str(self.weight)+")"


class Knapsack(OptimizableModel):
    def __init__(self, itemset, maxweight):
        self.maxweight = maxweight
        self.items = Optimizables.List(of=self, itemset=itemset, replicationrange=(0,1))
    
    @OptimizationPenalty("weights", 10)
    def totalWeight(self):
        totalweigth = sum([item.weight for item in self.items.val()])
        return totalweigth - self.maxweight if totalweigth > self.maxweight else 0
    
    @OptimizationObjective("value", 1)
    def totalValue(self):
        return sum([item.value for item in self.items.val()])
    
    def __str__(self):
        ret = str([str(item) for item in self.items.val()])+"\n"
        totalweigth = sum([item.weight for item in self.items.val()])
        ret += "Totale value: "+str(self.totalValue())+", Total weight: "+str(totalweigth)
        return ret

itemset = []
for _ in range(0,100):
    itemset.append(Item(random.randint(0,20), random.randint(0,20)))

opt = Optimizers.GeneticOptimizer(model=Knapsack, penalties=["weights"], objectives=["value"], args=(itemset, 500), maximize=True, convergenceWindow=150)
opt.runUntilConvergence()
print(opt.getResult())