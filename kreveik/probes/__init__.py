"""
Probes are objects that are meant to calculate and accumulate data from the
subroutines of the  simulation.
"""

import numpy as num 

class SubRoutine(object):
    def __init__ (self):
        pass
        
    
genetic_algorithm = SubRoutine()
genetic_iteration = SubRoutine()
populate_wildtype = SubRoutine()
populate_equilibria_in_family = SubRoutine()
populate_equilibria = SubRoutine()
search_equilibrium = SubRoutine()
advance = SubRoutine()


class probe (object):
    """
    Definition of the probe 
    A probe is has an assignee, and it is defined by listing a probe
    in the list "probes" within that object. (it can be a family or
    a network, obviously)
    The function is defined due to the Network 
    """
    def __init__ (self):
        self.function = None
        self.subroutine = None
        self.data = []

class family_mean_score_probe (probe):
    def __init__ (self):       
        probe.__init__(self)
        self.function = self.mean_score
        self.subroutine = genetic_iteration
        
    def mean_score(self,probeable):
        return num.mean(probeable.scores)
    
class mean_orbit_length_probe (probe):
    def __init__ (self):       
        probe.__init__(self)
        self.function = self.eq_score
        self.subroutine = populate_equilibria
        
    def eq_score(self,probeable):
        return [num.mean(probed.equilibria) for probed in probeable.network_list]
    
class motif_network_probe (probe):
    def __init__ (self,degree):       
        probe.__init__(self)
        self.function = self.motif_extractor
        self.subroutine = genetic_iteration
        self.degree = degree
        
    def motif_extractor(self,probeable):
        motif_out = probeable.motif_freqs(probeable,self.degree)
        return motif_out
    
class motif_family_probe (probe):
    def __init__ (self,degree,(first,last)):       
        probe.__init__(self)
        self.function = self.motif_extractor
        self.subroutine = genetic_iteration
        self.degree = degree
        self.first = first
        self.last = last
        
    def motif_extractor(self,probeable):
        return [network.motif_freqs(self.degree) for network 
                in probeable.network_list[self.first:self.last]]
        
