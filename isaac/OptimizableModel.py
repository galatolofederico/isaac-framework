from core import ControllerSingleton

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
    
    def deserialize(self, serialized):
        cs = ControllerSingleton()
        controller = cs.get()
        controller.deserializeObj(self, serialized)