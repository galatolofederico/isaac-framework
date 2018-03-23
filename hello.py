#! /usr/bin/env python

from isaac import Optimizables, OptimizableModel, OptimizationConstraint, Optimizers
import operator

def prod(iterable):
    return reduce(operator.mul, iterable, 1)


class Hello(OptimizableModel):
    def __init__(self):
        self.numbers = [Optimizables.IntRange(of=self, group="size", range=(0, 10)), 
        Optimizables.IntRange(of=self, group="size", range=(0, 10))]

    @OptimizationConstraint("hello", 1)
    def sum(self):
        return(abs(7 - sum([n.val() for n in self.numbers])))

    @OptimizationConstraint("hello", 1)
    def prod(self):
        return(abs(12 - prod([n.val() for n in self.numbers])))


opt = Optimizers.RandomOptimizer(model=Hello, constraints=["hello"])
opt.runUntilConvergence()
