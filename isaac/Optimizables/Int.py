from Optimizable import Optimizable
import random


class Int(Optimizable):
    """
    Description of Int

    """
    def __init__(self, **kargs):
        Optimizable.__init__(self, **kargs)
        if "range" not in kargs:
            raise Exception("You have to specify a 'range'")
        self.range = kargs["range"]
        self.new()
    def new(self):
        self.value = random.randrange(*self.range)