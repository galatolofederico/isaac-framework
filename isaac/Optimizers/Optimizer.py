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

    def epoch(self):
        raise NotImplementedError("An optimizer must have the epoch method")
    
    def hasFinished(self):
        raise NotImplementedError("An optimizer must have the hasFinished method")
    
    def getResult(self):
        raise NotImplementedError("An optimizer must have the getResult method")

    def getInstance(self):
        return self.model(*self.args)

    def __str__(self):
        #An optimizer should implement this
        return ""
    
    def runUntilConvergence(self, verbose=True):
        while not self.hasFinished():
            self.epoch()
            if verbose:
                sys.stdout.write(str(self))
    
    def runEpochs(self, n, verbose=True):
        for _ in range(0, n):
            self.epoch()
            if verbose:
                sys.stdout.write(str(self))


