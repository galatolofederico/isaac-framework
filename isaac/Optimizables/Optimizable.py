from .. import core

class Optimizable:
    """
You have to call this method in the constructor of the extended class
::
    class MyOptimizable(Optimizable):
        def __init__(self, **kargs):
            Optimizable.__init__(self, native, **kargs)

.. warning::
    This is an interface you should never use this class directly in your code but just extend it

"""
    def __init__(self, native = True, **kargs):
        r"""
:param native:
    False if you are creating a new Optimizable using existing Optimizables
:type first: ``bool``
:param \**kwargs:
    See below
:Keyword Arguments:
    * *of* (``ref``) --
        Refernce to the instance of which this Optimizable belongs
    * *group* (``str``) --
        Group in wich belong this Optimizable belongs
"""
        if "of" not in kargs:
            raise Exception("Every Optimizable must have at least the 'of' argument")
        self.of = kargs["of"]
        if "group" in kargs:
            self.group = kargs["group"]
        else:
            self.group = ""
        if native:
            if not hasattr(self.of, "_optimizablesGroups"):
                self.of._optimizablesGroups = core.OptimizableObject()
            self.of._optimizablesGroups.getGroup(self.group).addOptimizable(self)
    def val(self):
        return self.value
    def set(self, value):
        self.value = value
    def new(self):
        raise NotImplementedError("An Optimizable object must implement the new function")
