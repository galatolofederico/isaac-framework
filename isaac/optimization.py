from core import ControllerSingleton

class WeightedFunction:
    def __init__(self, weight, fn):
        self.weight = weight
        self.fn = fn
    def __str__(self):
        return "("+str(self.weight) + ", " + str(self.fn)+")"


class OptimizationPenalty(object):
    def __init__(self, groupName = "", weight = 1):
        self.groupName = groupName
        self.weight = weight
        cs = ControllerSingleton()
        self.controller = cs.get()
    
    def __call__(self, fn, *args, **kargs):
        self.controller.addPenalty(self.groupName, WeightedFunction(self.weight, fn))
        return fn

class OptimizationObjective(object):
    def __init__(self, groupName = "", weight = 1):
        self.groupName = groupName
        self.weight = weight
        cs = ControllerSingleton()
        self.controller = cs.get()
    
    def __call__(self, fn, *args, **kargs):
        self.controller.addObjective(self.groupName, WeightedFunction(self.weight, fn))
        return fn