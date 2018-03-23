from Optimizable import Optimizable
import random, string

class Char(Optimizable):
    def __init__(self, **kargs):
        Optimizable.__init__(self, **kargs)
        self.new()
    def new(self):
        self.value = random.choice(string.letters)