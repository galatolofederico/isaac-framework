from Optimizable import Optimizable
import random


class IntRange(Optimizable):
    def __init__(self, **kargs):
        Optimizable.__init__(self, **kargs)
        self.range = kargs["range"]
        self.new()
    def new(self):
        self.value = random.randrange(*self.range)