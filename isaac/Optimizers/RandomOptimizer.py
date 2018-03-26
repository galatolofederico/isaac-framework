from Optimizer import Optimizer

class RandomOptimizer(Optimizer):
    def __init__(self, **kargs):
        Optimizer.__init__(self, **kargs)
        randomobj = self.getInstance()
        ev = randomobj.evaluate(self.objectives, self.penalties, self.maximize)
        self.bestFitness = ev
        self.bestObj = randomobj

    def epoch(self):
        randomobj = self.getInstance()
        ev = randomobj.evaluate(self.objectives, self.penalties, self.maximize)
        if (ev < self.bestFitness and not self.maximize) or (ev > self.bestFitness and self.maximize):
            self.bestFitness = ev
            self.bestObj = randomobj
    
    def __str__(self):
        return "(bestFitness: "+str(self.bestFitness)+", bestObject: "+str(self.bestObj.serialize())+")\n"
    
    def getResult(self):
        return self.bestObj
    
    def getLastFitness(self):
        return self.bestFitness