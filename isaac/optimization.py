from core import ControllerSingleton

class Penalty:
    def __init__(self, weight, fn):
        self.weight = weight
        self.fn = fn
    def __str__(self):
        return "("+str(self.weight) + ", " + str(self.fn)+")"


class OptimizationPenalty(object):
    def __init__(self, of, weight):
        self.of = of
        self.weight = weight
        cs = ControllerSingleton()
        self.controller = cs.get()
    
    def __call__(self, fn, *args, **kargs):
        self.controller.addPenalty(self.of, Penalty(self.weight, fn))
        return fn
