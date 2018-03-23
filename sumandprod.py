#! /usr/bin/env python

from isaac import Optimizables, OptimizableModel, OptimizationConstraint, Optimizers
import operator

def prod(iterable):
    return reduce(operator.mul, iterable, 1)


#Find two numbers such that the sum is targetSum and product is targetProduct
class Hello(OptimizableModel):
    def __init__(self, targetSum, targetProduct):
        self.numbers = [Optimizables.IntRange(of=self, group="number", range=(0, 10)), 
        Optimizables.IntRange(of=self, group="number", range=(0, 10))]
        self.targetSum = targetSum
        self.targetProduct = targetProduct

    @OptimizationConstraint("hello", 1)
    def sum(self):
        return(abs(self.targetSum - sum([n.val() for n in self.numbers])))

    @OptimizationConstraint("hello", 1)
    def prod(self):
        return(abs(self.targetProduct - prod([n.val() for n in self.numbers])))


opt = Optimizers.RandomOptimizer(model=Hello, constraints=["hello"], args=(7, 12))
opt.runUntilConvergence()
