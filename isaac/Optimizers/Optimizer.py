import sys

class Optimizer:
    def __init__(self, **kargs):
        if "model" not in kargs or "constraints" not in kargs:
            raise Exception("You have to specify a model and a constraints group")
        self.model = kargs["model"]
        self.constraints = kargs["constraints"]

    def epoch(self):
        raise NotImplementedError("An optimizer must have the epoch method")
    
    def hasFinished(self):
        raise NotImplementedError("An optimizer must have the hasFinished method")
    
    def __str__(self):
        #An optimizer should implement this
        return ""
    
    def runUntilConvergence(self, verbose=True):
        while not self.hasFinished():
            self.epoch()
            if verbose:
                sys.stdout.write(str(self))


