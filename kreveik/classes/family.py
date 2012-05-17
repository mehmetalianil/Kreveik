"""
This module includes the class definitions concerning the Family.

"""
import numpy as num
import matplotlib.pyplot as plt
import logging
from kreveik.classes import *
import kreveik.probes as probes


class Family(ProbeableObj,Ensemble):
    '''
    Family
    ======
    
    A Family object is a holder of many networks. It is meant to simplify the actions taken concerning a group of
    network, to simplify the characterization of an ensemble, and record primary parameters.
    '''
    
    def __init__ (self):
        ProbeableObj.__init__(self)
        Ensemble.__init__(self)
        self.network_list = []
        self.wildtype_list = [] 
        self.scores = num.array([])        
            
    def __getitem__(self, index):
        """
        Returns the nth item of a Family.
        """
        if index > len(self.network_list):
            raise IndexError
        return self.network_list[index]
    
    def __contains__(self, network):
        """
        Returns a boolean according to whether a family includes a network  
        """
        return network in self.network_list
        
    def __len__ (self):
        """
        Returns the population of the Family. 
        """
        return len(self.network_list)
    
    def remove(self,n):
        """
        Removes the nth individual from the family.
        """
        self.network_list = num.delete(self.network_list, n).tolist()
                
    def add(self, network):
        '''
        This method will add a network to the specified family.
        '''
        
        if network in self.network_list:
            logging.warning("The network that you're trying to add to the family is already a member.\
            Please clone the individual and append the clone, if this is necessary.")
            return False
        
        self.network_list.append(network)
        return True
            
    def plot_scores(self):
        """
        Plots the scores of the individuals within the family.
        This right now works if the scores of the individuals are populated with 
        family_name.populate_equilibria().
        
        This will be subject to a change: 
           Properties such as scores, or equilibria will be held in dictionaries, in order to 
           easily distinguish families or networks that have ondergone a procedure (scoring, for example.)
           or not. This will give us the opportunity to check such flags and act accordingly.
        """
        plt.plot(self.scores)
        plt.show()
    
    def populate_equilibria(self):
        '''
        If the family has individuals, it goes to each individual and finds the equilibria 
        for all possible initial conditions they may face. The orbits and scores are 
        assigned to each one of them.
        '''
        
        if len(self.network_list) == 0:
            logging.warning("Warning: There is nobody in this family.Please adopt individuals.")
            return False
            
        self.scores = num.zeros(len(self.network_list))
       
        for counter,network in enumerate(self.network_list): 
            logging.info("("+str(counter+1)+"/"+str(len(self.network_list))
                         +") Populating equilibrium for: "+str(network))
            network.populate_equilibria()
            self.scores[counter] = network.score
            
        self.populate_probes(probes.populate_equilibria_in_family)
            


