import sys

class Optimizer:
    def __init__(self, **kargs):
        if "model" not in kargs:
            raise Exception("You have to specify at least a model to optimize")
        self.model = kargs["model"]
        self.constraints = [""]
        if "constraints" in kargs:
            self.constraints += kargs["constraints"]
        self.args = ()
        if "args" in kargs:
            self.args = kargs["args"]
        self.maximize = False
        if "maximize" in kargs:
            self.maximize = kargs["maximize"]
        self.convergenceWindow = 100
        if "convergenceWindow" in kargs:
            self.convergenceWindow = kargs["convergenceWindow"]

    def epoch(self):
        raise NotImplementedError("An optimizer must have the epoch method")
    
    def getResult(self):
        raise NotImplementedError("An optimizer must have the getResult method")
    
    def getLastFitness(self):
        raise NotImplementedError("An optimizer must have the getLastFitness method")

    def getInstance(self):
        return self.model(*self.args)

    def __str__(self):
        #An optimizer should implement this
        return ""
    
    def runUntilConvergence(self, verbose=True):
        lastFitness = None
        convergenceCount = 0
        while True:
            self.epoch()
            if verbose:
                sys.stdout.write(str(self))
            if self.getLastFitness() == lastFitness:
                convergenceCount += 1
            else:
                convergenceCount = 0
            if convergenceCount >= self.convergenceWindow:
                return
            lastFitness = self.getLastFitness()
    
    def runEpochs(self, n, verbose=True):
        for _ in range(0, n):
            self.epoch()
            if verbose:
                sys.stdout.write(str(self))


