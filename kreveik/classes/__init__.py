'''
The genereg package maintains class definitions and methods for manipulation,
statistical evaluation of random boolean networks. The emphasis is upon genetic
algorithm and how networks evolve accordingly.
'''

import numpy as num
import matplotlib.pyplot as plt
import copy
from baseclasses import ProbeableObj,Ensemble,Element
from network import TopologicalNetwork,Motif,Network
from family import Family

__all__ =['baseclasses','family','network']
