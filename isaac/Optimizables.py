import core
import random

class Optimizable:
    def __init__(self, **kargs):
        self.of = kargs["of"]
        if "group" in kargs:
            self.group = kargs["group"]
        else:
            self.group = ""
        core.controller.add(of=self.of, group=self.group, optimizable=self)
    def val(self):
        return self.value
    def set(self, value):
        self.value = value
    def new(self):
        pass


class Optimizables:
    def __init__(self):
        pass
    class IntRange(Optimizable):
        def __init__(self, **kargs):
            Optimizable.__init__(self, **kargs)
            self.range = kargs["range"]
            self.new()
        def new(self):
            self.value = random.randrange(*self.range)