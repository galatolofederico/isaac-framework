from .. import core

class Optimizable:
    def __init__(self, native = True, **kargs):
        if "of" not in kargs:
            raise Exception("Every Optimizable must have at least the 'of' argument")
        self.of = kargs["of"]
        if "group" in kargs:
            self.group = kargs["group"]
        else:
            self.group = ""
        if native:
            if not hasattr(self.of, "_optimizablesGroups"):
                self.of._optimizablesGroups = core.OptimizableObject()
            self.of._optimizablesGroups.getGroup(self.group).addOptimizable(self)
    def val(self):
        return self.value
    def set(self, value):
        self.value = value
    def new(self):
        raise NotImplementedError("An Optimizable object must implement the new function")
