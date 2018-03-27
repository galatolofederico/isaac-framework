#! /usr/bin/env python
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
from isaac import *
import operator

def prod(iterable):
    return reduce(operator.mul, iterable, 1)


#Find two numbers such that the sum is targetSum and product is targetProduct
class SumProd(OptimizableModel):
    def __init__(self, targetSum, targetProduct):
        self.numbers = [Optimizables.Int(of=self, group="number", range=(0, 10)), 
        Optimizables.Int(of=self, group="number", range=(0, 10))]
        self.targetSum = targetSum
        self.targetProduct = targetProduct

    @OptimizationObjective("sumprod")
    def sum(self):
        return(abs(self.targetSum - sum([n.val() for n in self.numbers])))

    @OptimizationObjective("sumprod")
    def prod(self):
        return(abs(self.targetProduct - prod([n.val() for n in self.numbers])))


opt = Optimizers.RandomOptimizer(model=SumProd, objectives=["sumprod"], args=(7, 12))
opt.runUntilConvergence()
