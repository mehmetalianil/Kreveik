
#    Copyright 2012 Mehmet Ali ANIL
#    
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#    
#    http://www.apache.org/licenses/LICENSE-2.0
#    
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""
Module that maintains classes concerning Family objects. 
"""

import other
import logging
import numpy as num
import matplotlib.pyplot as plt
import kreveik
import copy

class Family(other.ProbeableObj,other.Ensemble):
    '''
    Family Class.
    A class that will have a single family of networks, a genetic algorithm 
    will be run within a family. The macro parameters of a group of network, 
    though may also be reached from a list of networks, will be housed in a 
    family in a more structured manner.
    '''
    
    def __init__ (self):
        other.ProbeableObj.__init__(self)
        other.Ensemble.__init__(self)
        self.network_list = []
        self.wildtype_list = [] 
        self.scores = num.array([])
        self.scores_history = []
        
            
    def __getitem__(self, index):
        """
        nth item of a Family object returns the nth network it has
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
        return len(self.network_list)
    
    def remove(self,n):
        """
        removes the nth network from the family
        """
        self.network_list = num.delete(self.network_list, n).tolist()
                
    def add(self, network):
        '''
        This method will add a network to the specified family.
        network -> The network that is to be appended to the family.
        '''
        
        if network in self.network_list:
            logging.warning("The network that you're trying to add to the family is already a member.\
            Please clone the individual and append the clone.")
            return False
        
        self.network_list.append(network)
        return True
            
    def copy(self):
        """
        Returns a copy of the Family object. 
        """
        return copy.deepcopy(self)
    
    def remove_all_self_connections(self):
        """
        Removes self connections of the nodes in every network of a family.
        """
        for network in self:
            network.remove_self_connection()
            
    def plot_scores(self):
        """
        If family.populate_equilibria is used to extract scores of all networks within a family,
        this function will plot the scores of each network.
        """
             
        plt.plot(self.scores)
        plt.show()
    
    def populate_equilibria(self,pp=False):
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
        self.populate_probes(kreveik.probes.populate_equilibria_in_family)
            


