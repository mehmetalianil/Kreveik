"""
Definition of the family class
"""

from baseclasses import *
from network import *
import numpy as num
import matplotlib.pyplot as plt
import copy
import networkx as nx
from ..probes import *
import itertools

verbose=True
debug=False

class Family(ProbeableObj):
    '''
    Family Class.
    A class that will have a single family of networks, a genetic algorithm 
    will be run within a family. The macro parameters of a group of network, 
    though may also be reached from a list of networks, will be housed in a 
    family in a more structured manner.
    '''
    
    def __init__ (self):
        ProbeableObj.__init__(self)
        self.network_list = []
        self.wildtype_list = [] 
        self.scores = num.array([])
        self.scores_history = []
    
    def add_to_family(self, network):
        '''
        This method will add a network to the specified family.
        network -> The network that is to be appended to the family.
        '''
        
        if network in self.network_list:
            print "The network that you're trying to add to the family is already a member."
            print "Please clone the individual and append the clone."
            return False
        
        self.network_list.append(network)
        return True
            
    def plot_scores(self):
             
        plt.plot(self.scores)
        plt.show()
    
    def populate_equilibria_in_family(self):
        '''
        If the family has individuals, it goes to each individual and finds the equilibria 
        for all possible initial conditions they may face. The orbits and scores are 
        assigned to each one of them.
        '''
        
        if len(self.network_list) == 0:
            print "Warning: There is nobody in this family."
            print "Please adopt individuals."
            return False
            
        self.scores = num.zeros(len(self.network_list))
        
        for id,network in enumerate(self.network_list): 
            if verbose:
                print "("+str(id+1)+"/"+str(len(self.network_list))+") Populating equilibrium for: "+str(network)
            network.populate_equilibria()
            self.scores[id] = network.score
        self.populate_probes(probes.populate_equilibria_in_family)
            

    def motif_freqs(self,degree):
        """
        Returns a list of motifs of the family.
        """
        motif_list = []
        
        for (enum,network) in enumerate(self.network_list):
            all_combinations = itertools.combinations(range(len(network.adjacency)),degree)
            if verbose:
                print "Extracting motifs of Network #"+str(enum)+" of "+str(len(self.network_list))
            for combination in all_combinations:
            
                this_motif_adj = num.zeros((degree,degree))
                for (first_ctr,first_node) in enumerate(list(combination)):
                    for (second_ctr,second_node) in enumerate(list(combination)):
                        this_motif_adj[first_ctr][second_ctr] = network.adjacency[first_node][second_node]
                
                this_motif = Motif(this_motif_adj)
    
                if this_motif.is_connected():                
                    truth = [this_motif == old_motif for old_motif in motif_list]
                    if (any(truth) == True):
                        index = truth.index(True)
                        motif_list[index].freq = motif_list[index].freq+1
                    elif (all(truth) == False) or (len(truth)==0):
                        motif_list.append(this_motif)
                    else:
                        print "There has been a problem while extracting Motifs"
                        break
                
        return motif_list

