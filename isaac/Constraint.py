from core import *

cs = ControllerSingleton()
controller = cs.get()


class Constraint:
    def __init__(self, weight, fn):
        self.weight = weight
        self.fn = fn
    def __str__(self):
        return "("+str(self.weight) + ", " + str(self.fn)+")"


class OptimizationConstraint(object):
    def __init__(self, of, weight):
        self.of = of
        self.weight = weight
    
    def __call__(self, fn, *args, **kargs):
        global controller
        controller.addConstraint(self.of, Constraint(self.weight, fn))