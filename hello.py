#! /usr/bin/env python

from __future__ import print_function
from isaac import Optimizables, OptimizableModel, OptimizationConstraint, Optimizers


def editDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

#The array words should be equal to ["hello", "world"]
class Hello(OptimizableModel):
    def __init__(self):
        #Initialize the list words with two lists of size 5 filled with Optmizables.Char
        self.words = [[Optimizables.Char(of=self, group="first_word") for _ in range(0, 5)]
        ,[Optimizables.Char(of=self, group="second_word") for _ in range(0, 5)]]
    
    @OptimizationConstraint("hello", 1)
    def first_word(self):
        #Compute the distance between the first word and "hello"
        word = "".join([c.val() for c in self.words[0]])
        return editDistance(word, "hello")

    @OptimizationConstraint("hello", 1)
    def second_word(self):
        #Compute the distance between the first word and "world"
        word = "".join([c.val() for c in self.words[1]])
        return editDistance(word, "world")



opt = Optimizers.GeneticOptimizer(model=Hello, constraints=["hello"])
opt.runUntilConvergence()
print([[c.val() for c in w] for w in opt.getResult().words])