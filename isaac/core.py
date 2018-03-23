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

class OptimizableModel:
    def __del__(self):
        cs = ControllerSingleton()
        controller = cs.get()
        controller.remove(self)
    
    def evaluate(self, constraints):
        cs = ControllerSingleton()
        controller = cs.get()
        ret = 0
        for constraintgroup in constraints:
            if constraintgroup in controller.constraints:
                for constraint in controller.constraints[constraintgroup]:
                    ret += constraint.weight * constraint.fn(self)
        return ret

    def serialize(self):
        cs = ControllerSingleton()
        controller = cs.get()
        return controller.serializeObj(self)


class ControllerSingleton:
    singleton = None
    def __init__(self):
        if ControllerSingleton.singleton == None:
            ControllerSingleton.singleton = OptimizationController()
    
    def get(self):
        return ControllerSingleton.singleton

cs = ControllerSingleton()
controller = cs.get()