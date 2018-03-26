from core import ControllerSingleton
import random, warnings

class OptimizableModel:
    def __del__(self):
        cs = ControllerSingleton()
        controller = cs.get()
        controller.remove(self)
    
    def compute(self, objectives, penalties):
        cs = ControllerSingleton()
        controller = cs.get()
        totalpenalties = 0
        totalobjectives = 0
        for penaltygroup in penalties:
            if penaltygroup in controller.penalties:
                for penalty in controller.penalties[penaltygroup]:
                    totalpenalties += penalty.weight * penalty.fn(self)
            else:
                warnings.warn("The peanlty group '"+penaltygroup+"' do not exist")
                
        for objectivegroup in objectives:
            if objectivegroup in controller.objectives:
                for objective in controller.objectives[objectivegroup]:
                    totalobjectives += objective.weight * objective.fn(self)
            else:
                warnings.warn("The objective group '"+objectivegroup+"' do not exist")
             
        self.results = [totalobjectives, totalpenalties]
    
    def evaluate(self, objectives, penalties, maximize):
        self.compute(objectives, penalties)
        if maximize:
            return self.results[0] - self.results[1]
        else:
            return self.results[0] + self.results[1]


    def serialize(self):
        cs = ControllerSingleton()
        controller = cs.get()
        return controller.serializeObj(self)
    
    def deserialize(self, serialized):
        cs = ControllerSingleton()
        controller = cs.get()
        controller.deserializeObj(self, serialized)
    
    def mutation(self):
        cs = ControllerSingleton()
        controller = cs.get()
        obj = controller.getObject(self)
        grp = obj.groups[random.choice(obj.groups.keys())]
        opt_i = random.choice(range(0, len(grp.optimizables)))
        grp.optimizables[opt_i].new()

