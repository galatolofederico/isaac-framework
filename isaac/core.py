class OptimizableGroup:
    def __init__(self):
        self.optimizables = []

    def addOptimizable(self, opt):
        self.optimizables.append(opt)

    def serialize(self):
        return [o.val() for o in self.optimizables]

    def deserialize(self, ser):
        if len(ser) != len(self.optimizables):
            raise Exception("Trying to deserialize different objects in size")
        for i, v in enumerate(ser):
            self.optimizables[i].set(v)

class OptimizableObject:
    def __init__(self):
        self.groups = {}
        self.penalties = []
        
    def getGroup(self, name):
        if name in self.groups:
            return self.groups[name]
        self.groups[name] = OptimizableGroup()
        return self.groups[name]


class OptimizationController:
    def __init__(self):
        self.objects = {}
        self.penalties = {}
        self.objectives = {}

    def _addToHT(self, ht, groupName, c):
        if groupName not in ht:
            ht[groupName] = []
        if c not in ht[groupName]:
            ht[groupName].append(c)

    def addPenalty(self, groupName, c):
        self._addToHT(self.penalties, groupName, c)

    def addObjective(self, groupName, c):
        self._addToHT(self.objectives, groupName, c)


class ControllerSingleton:
    singleton = None
    def __init__(self):
        if ControllerSingleton.singleton == None:
            ControllerSingleton.singleton = OptimizationController()
    
    def get(self):
        return ControllerSingleton.singleton
