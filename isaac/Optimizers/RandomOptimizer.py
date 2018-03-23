from Optimizer import Optimizer

class RandomOptimizer(Optimizer):
    def __init__(self, **kargs):
        Optimizer.__init__(self, **kargs)
        self.bestFitness = 2**32
        self.bestObj = None

    def epoch(self):
        randomobj = self.getInstance()
        ev = randomobj.evaluate(self.constraints)
        if ev < self.bestFitness:
            self.bestFitness = ev
            self.bestObj = randomobj
    
    def __str__(self):
        return "(bestFitness: "+str(self.bestFitness)+", bestObject: "+str(self.bestObj.serialize())+")\n"
    
    def hasFinished(self):
        return self.bestFitness == 0
    
    def getResult(self):
        return self.bestObj