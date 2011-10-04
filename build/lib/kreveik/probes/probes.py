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
        self.data = num.array([])

class mean_score_probe (probe):
    def __init__ (self):       
        probe.__init__(self)
        self.function = self.mean_score
        self.subroutine = genetic_iteration
        
    def mean_score(self,probeable):
        return num.mean(probeable.scores)
    
class eq_score_probe (probe):
    def __init__ (self):       
        probe.__init__(self)
        self.function = self.eq_score
        self.subroutine = populate_equilibria
        
    def eq_score(self,probeable):
        print  [num.mean(probed.equilibria) for probed in probeable.network_list]
        return [num.mean(probed.equilibria) for probed in probeable.network_list]

