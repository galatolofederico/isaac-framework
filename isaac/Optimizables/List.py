from Int import Int
from Optimizable import Optimizable

class List(Optimizable):
    def __init__(self, **kargs):
        Optimizable.__init__(self, False, **kargs)
        if "itemset" not in kargs or "replicationrange" not in kargs:
            raise Exception("An Optimizable.List must have an 'itemset' and a 'replicationrange'")
        self.itemset = kargs["itemset"]
        self.range = kargs["replicationrange"]
        self.list = [Int(of=self.of, group=self.group, range=(self.range[0], self.range[1]+1)) for _ in range(0, len(self.itemset))]
    
    def new(self):
        for item in self.list:
            item.new()
    
    def val(self):
        counts = [item.val() for item in self.list]
        ret = []
        for i,count in enumerate(counts):
            ret += [self.itemset[i] for _ in range(0, count)]
        return ret
    
    def set(self):
        raise Exception("Not yet implemented")
