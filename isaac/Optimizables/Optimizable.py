from .. import core

class Optimizable:
    def __init__(self, **kargs):
        self.of = kargs["of"]
        if "group" in kargs:
            self.group = kargs["group"]
        else:
            self.group = ""
        cs = core.ControllerSingleton()
        self.controller = cs.get()
        self.controller.add(of=self.of, group=self.group, optimizable=self)
    def val(self):
        return self.value
    def set(self, value):
        self.value = value
    def new(self):
        pass
