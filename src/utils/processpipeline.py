"""
Pipeline module
"""
from functools import reduce


class ProcessPipeline:
    """
    ProcessPipeline that performs a chain of functions on a given input. Input and output should
    always have
    the same type.
    """

    @staticmethod
    def identity(x):
        return x

    def __init__(self, fcts=None):
        self._functions = []
        self.register(ProcessPipeline.identity)
        if fcts is not None:
            self.register(fcts)

    def register(self, fcts):
        if isinstance(fcts, list):
            self._register_list(fcts)
        elif callable(fcts):
            self._register_function(fcts)
        else:
            raise Exception('Given object was neither list nor object.')

    def _register_list(self, fcts):
        for fct in fcts:
            self._register_function(fct)

    def _register_function(self, fct):
        if callable(fct):
            self._functions.append(fct)

    def execute(self, inp):
        return reduce(lambda val, fun: fun(val), self._functions, inp)


