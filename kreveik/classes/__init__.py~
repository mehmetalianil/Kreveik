'''
The genereg package maintains class definitions and methods for manipulation,
statistical evaluation of random boolean networks. The emphasis is upon genetic
algorithm and how networks evolve accordingly.
'''

import numpy as num
import matplotlib.pyplot as plt
import logging

class ProbeableObj (object):
    """Base class for objects that a Probe object can be attached. 
    """
    def __init__ (self):
        self.probes = []
    def attach (self,probe):
        if probe in self.probes:
            logging.warning('The probe is already attached.')
        else:
            self.probes.append(probe)
    def __call__(self,probed):
        self.attach(probed)
         
    def populate_probes (self,subroutine):
        for probe in self.probes:
            if probe.subroutine == subroutine:
                measured = probe.function(self)
                probe.data.append(measured)
                
class Ensemble(object):
    """Base class for all that are going to be used as an ensemble of elements that are subject to 
    Genetical Algorithm
    """
    def __init__(self):
        self.scorer = None
        self.selector = None
        self.mutator = None
        self.killer = None
        
class Element(object):
    """Base class for all that are going to be used as individuals within an element in a Genetical 
    Algorithm
    """
    def __init__(self):
        self.score = None
        self.mutated = 0
        self.parent = None
        self.children = []


from network import TopologicalNetwork,Motif,Network
from family import Family


