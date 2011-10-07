'''
Created on 09.02.2011

@author: Mehmet Ali Anil

The genereg package maintains class definitions and methods for manipulation,
statistical evaluation of random boolean networks. The emphasis is upon genetic
algorithm and how networks evolve accordingly.
'''


import numpy as num
import matplotlib.pyplot as plt
import copy
import networkx as nx

print_enable=True


__author__ = "Mehmet Ali Anil"
__copyright__ = ""
__credits__ = ["Mehmet Ali Anil"]
__license__ = ""
__version__ = "0.0.5"
__maintainer__ = "Mehmet Ali Anil"
__email__ = "anilm@itu.edu.tr"
__status__ = "Production"

from baseclasses import *
from network import *
from family import *
from generators import *

