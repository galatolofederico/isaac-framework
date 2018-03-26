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
    def __init__(self, ref):
        self.groups = {}
        self.penalties = []
        self.ref = ref
        
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
    
    def deserializeObj(self, obj, serialized):
        obj = self.getObject(obj)
        for key in obj.groups:
            obj.groups[key].deserialize(serialized[key])


class ControllerSingleton:
    singleton = None
    def __init__(self):
        if ControllerSingleton.singleton == None:
            ControllerSingleton.singleton = OptimizationController()
    
    def get(self):
        return ControllerSingleton.singleton
