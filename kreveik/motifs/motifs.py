'''
Created on Sep 11, 2011
'''

from classes import *

class Motif (Network):
    def __init__ (self):
        Network.__init__(self, adjacency_matrix, mask, score, function, state_vec)
    