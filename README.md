# Isaac Optimization Framework

Isaac was born with the intent to fill the **gap** between **high level description** capabilities of the modern programming languages and the **optimizations algorithms**.
With isaac you can model your optimization problems using all the expressive power of Python; You just need to **substitute** the **parameters** that you want to **optimize** with the Isaac's **placeholders** and **run** the algorithm that you prefer.

## Documentation

Work in progress

## Examples

#### Hello World with genetic algorithm
```python
#The array words should be equal to ["hello", "world"]
class Hello(OptimizableModel):
    def __init__(self):
        #Initialize the list words with two lists of size 5 filled with Optmizables.Char
        self.words = [[Optimizables.Char(of=self, group="first_word") for _ in range(0, 5)],
        [Optimizables.Char(of=self, group="second_word") for _ in range(0, 5)]]
    
    @OptimizationConstraint("hello", 1)
    def first_word(self):
        #Compute the distance between the first word and "hello"
        word = "".join([c.val() for c in self.words[0]])
        return editDistance(word, "hello")

    @OptimizationConstraint("hello", 1)
    def second_word(self):
        #Compute the distance between the first word and "world"
        word = "".join([c.val() for c in self.words[1]])
        return editDistance(word, "world")

opt = Optimizers.GeneticOptimizer(model=Hello, constraints=["hello"])
opt.runUntilConvergence()
print([[c.val() for c in w] for w in opt.getResult().words])
```
#### Two numbers knowing sum and product with randomic search

```python
#Find two numbers such that the sum is targetSum and product is targetProduct
class SumProd(OptimizableModel):
    def __init__(self, targetSum, targetProduct):
        self.numbers = [Optimizables.Int(of=self, group="number", range=(0, 10)), 
        Optimizables.Int(of=self, group="number", range=(0, 10))]
        self.targetSum = targetSum
        self.targetProduct = targetProduct

    @OptimizationConstraint("sumprod", 1)
    def sum(self):
        return(abs(self.targetSum - sum([n.val() for n in self.numbers])))

    @OptimizationConstraint("sumprod", 1)
    def prod(self):
        return(abs(self.targetProduct - prod([n.val() for n in self.numbers])))


opt = Optimizers.RandomOptimizer(model=SumProd, constraints=["sumprod"], args=(7, 12))
opt.runUntilConvergence()
```
#### Binary knapsack problem with genetic algorithm

```python
class Item:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight
    
    def __str__(self):
        return "(value: "+str(self.value)+", weight: "+str(self.weight)+")"


class Knapsack(OptimizableModel):
    def __init__(self, itemset, maxweight):
        self.maxweight = maxweight
        self.items = Optimizables.List(of=self, itemset=itemset, replicationrange=(0,1))
    
    @OptimizationConstraint("weights", 1)
    def totalWeight(self):
        totalweigth = sum([item.weight for item in self.items.val()])
        return totalweigth if totalweigth <= self.maxweight else -2**32
    
    @OptimizationConstraint("value", 1)
    def totalValue(self):
        return sum([item.value for item in self.items.val()])
    
    def __str__(self):
        ret = str([str(item) for item in self.items.val()])+"\n"
        ret += "Totale value: "+str(self.totalValue())+", Total weight: "+str(self.totalWeight())
        return ret

itemset = []
for _ in range(0,100):
    itemset.append(Item(random.randint(0,20), random.randint(0,20)))

opt = Optimizers.GeneticOptimizer(model=Knapsack, constraints=["weights", "value"], args=(itemset, 500), maximize=True, convergenceWindow=150)
opt.runUntilConvergence()
print(opt.getResult())
```