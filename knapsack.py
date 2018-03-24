#! /usr/bin/env python

from __future__ import print_function
from isaac import Optimizables, OptimizableModel, OptimizationConstraint, Optimizers
import random

class Item:
    def __init__(self, knapsack, value, weight):
        self.value = value
        self.weight = weight
        self.inKnapsack = Optimizables.Bool(of=knapsack, group="items")
    
    def __str__(self):
        return "(value: "+str(self.value)+", weight: "+str(self.weight)+")"


class Knapsack(OptimizableModel):
    def __init__(self, maxweight):
        self.maxweight = maxweight
        self.items = []
        for _ in range(0,100):
            self.items.append(Item(self, random.randint(0,20), random.randint(0,20)))
    
    @OptimizationConstraint("weights", 1)
    def totalWeight(self):
        totalweigth = sum([item.weight if item.inKnapsack.val() else 0 for item in self.items])
        return totalweigth if totalweigth <= self.maxweight else -2**32
    
    @OptimizationConstraint("value", 1)
    def totalValue(self):
        return sum([item.value if item.inKnapsack.val() else 0 for item in self.items])
    
    def __str__(self):
        ret = str([str(item) for item in self.items if item.inKnapsack.val()])+"\n"
        ret += "Totale value: "+str(self.totalValue())+", Total weight: "+str(self.totalWeight())
        return ret


opt = Optimizers.GeneticOptimizer(model=Knapsack, constraints=["weights", "value"], args=(500,), maximize=True)
opt.runEpochs(200)
print(opt.getResult())