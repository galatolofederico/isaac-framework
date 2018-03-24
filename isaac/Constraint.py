from core import ControllerSingleton

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
        cs = ControllerSingleton()
        self.controller = cs.get()
    
    def __call__(self, fn, *args, **kargs):
        self.controller.addConstraint(self.of, Constraint(self.weight, fn))
        return fn