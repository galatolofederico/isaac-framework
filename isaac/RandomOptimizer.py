class RandomOptimizer:
    def __init__(self, model, constraints):
        self.model = model
        self.constraints = constraints
        self.bestEv = 2**32
        self.bestObj = None

    def epoch(self):
        randomobj = self.model()
        ev = randomobj.evaluate(self.constraints)
        if ev < self.bestEv:
            self.bestEv = ev
            self.bestObj = randomobj