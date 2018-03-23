class OptimizableGroup:
    def __init__(self):
        self.optimizables = []
    def addOptimizable(self, opt):
        self.optimizables.append(opt)
    def serialize(self):
        return [o.val() for o in self.optimizables]

class OptimizableObject:
    def __init__(self, ref):
        self.groups = {}
        self.constraints = []
        self.ref = ref
    def getGroup(self, name):
        if name in self.groups:
            return self.groups[name]
        self.groups[name] = OptimizableGroup()
        return self.groups[name]


class OptimizationController:
    def __init__(self):
        self.objects = {}
        self.constraints = {}

    def addConstraint(self, objname, c):
        if objname not in self.constraints:
            self.constraints[objname] = []
        if c not in self.constraints[objname]:
            self.constraints[objname].append(c)

    def getObject(self, ref):
        hash = id(ref)
        if hash in self.objects:
            return self.objects[hash]
        self.objects[hash] = OptimizableObject(ref)
        return self.objects[hash]
    
    def removeObject(self, hash):
        del self.objects[hash]

    def add(self, **kargs):
        obj = self.getObject(kargs["of"])
        grp = obj.getGroup(kargs["group"])
        grp.addOptimizable(kargs["optimizable"])
    
    def remove(self, of):
        self.removeObject(id(of))
    
    def serializeObj(self, obj):
        obj = self.getObject(obj)
        serialized = {}
        for key in obj.groups:
            serialized[key] = obj.groups[key].serialize()
        return serialized


class ControllerSingleton:
    singleton = None
    def __init__(self):
        if ControllerSingleton.singleton == None:
            ControllerSingleton.singleton = OptimizationController()
    
    def get(self):
        return ControllerSingleton.singleton
