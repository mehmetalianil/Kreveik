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

print_enable=True
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
        
        # Wont go on unless the Window is closed.
        plt.show()
        
    def populate_wildtype(self,wildtype_threshold):
        '''
        Finds the wild types in a family and populates the list wildtype_list with them.
        Input Arguments
            wildtype_threshold -> a threshold for the score of he individual in order to attend
            the wildtype club.
        '''
        if len(self.scores) == 0:
            if print_enable:
                print "Warning: Equilibria not found."
                print "Populating equilibria ..."
            self.populate_equilibria_in_family()
            if print_enable:
                print "    Done!"
        
        print "Checking individuals in this family by their scores"
        for network in self.network_list:
            if network.score == 0:
                if print_enable:
                    print "Warning: Network "+str(network)+" has no information on its equilibrium"
                    print "Now calculating its equilibria..."
                network.populate_equilibria()
                if print_enable:    
                    print "    Done!"
                
            if network.score < wildtype_threshold:
                if print_enable:
                    print "Network "+str(id(network))+" is wild."
                self.wildtype_list.append(network)
        
        self.populate_probes(probes.populate_wildtype)
        return True
    
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
            if print_enable:
                print "("+str(id+1)+"/"+str(len(self.network_list))+") Populating equilibrium for: "+str(network)
            network.populate_equilibria()
            self.scores[id] = network.score
        self.populate_probes(probes.populate_equilibria_in_family)
            
    def genetic_iteration(self,score_threshold,mutant_recipe=('Both',1),howmany_gntc=1):
        '''
        Runs one iteration of the genetic algorithm.
        It finds wildtypes of the family, mutates them, populates the family with mutants
        and assasinates as much of it has mutated. 
        '''
        if self.wildtype_list != []:
            self.wildtype_list = []
        if print_enable:
            print "Determining wildtypes"
        self.populate_wildtype(score_threshold)
        if print_enable:
            print str(len(self.wildtype_list))+"wild individuals"
        kill_count = len(self.wildtype_list)
        family_count = len(self.network_list)
        
        #    Prepare a vector that has ones for each to be killed, zeroes for all remain.
        #    and permute its elements randomly.
        
        array = [1]*kill_count+[0]*(family_count-kill_count)
 
        random_kill_list = num.random.permutation(array)
        
        #    Tag each element as None for those who'll be killed
        
        for number,to_be_killed in enumerate(random_kill_list):
            if to_be_killed == 1:
                if print_enable:
                    print str(self.network_list[number])+" is killed with score"+str(self.network_list[number].score) 
                self.network_list[number] = None
                
        #    If there are ones that are killed, populate the remaining gaps with mutated wildtypes.
        counter_wt = 0
        
        for network_ctr,all_networks in enumerate(self.network_list):
            if all_networks == None:
                if print_enable:
                    print "mutating network "+str(self.wildtype_list[counter_wt])
                self.network_list[network_ctr] = self.wildtype_list[counter_wt].mutant(mutated_obj=mutant_recipe,howmany=howmany_gntc)[0]
                if print_enable:    
                    print "finding equilibria of the new network "+str(self.network_list[network_ctr])
                self.network_list[network_ctr].populate_equilibria()
                self.scores[network_ctr] = self.network_list[network_ctr].score
                counter_wt = counter_wt +1
                
        self.scores_history = num.append(self.scores_history,self.scores)
        self.populate_probes(probes.genetic_iteration)
        return self.scores
        
    def motif_freqs(self,degree):
        """
        Returns a list of motifs of the family.
        """
        motif_list = []
        
        for (enum,network) in enumerate(self.network_list):
            all_combinations = itertools.combinations(range(len(network.adjacency)),degree)
            if print_enable:
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

    def genetic_algorithm(self,howmany=5,*args,**kwargs):
        """
        The wrapper for consecutive genetic iterations.
        """
        self.populate_equilibria_in_family()
        
        for ctr in range(howmany[0]):
            meanscore = self.scores.mean()
            if print_enable:
                print "Iteration "+str(ctr)+" Mean Score is: "+str(meanscore)
            self.genetic_iteration(meanscore,howmany[1])
        self.populate_probes(probes.genetic_algorithm)

