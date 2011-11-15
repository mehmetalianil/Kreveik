import numpy as num
import itertools
from mutator import *

def score(network,scorer=None):
    """
    If a scorer is specified, the score of the network calculated with that
    scorer is returned. 
    If scorer is not set, then the network is scored implicitly,
    """
    if scorer == None:
        network.score = network.scorer(network)
    else
        return scorer(network)
    
def motif_freqs (network,degree):
        """
        Returns a list of motifs.
        """
    
        all_combinations = itertools.combinations(range(len(network.adjacency)),degree)
        motif_list = []
        
        for combination in all_combinations:
            if debug: 
                print "Motif Permutation:"+str(list(combination))
            
            this_motif_adj = num.zeros((degree,degree))
            for (first_ctr,first_node) in enumerate(list(combination)):
                for (second_ctr,second_node) in enumerate(list(combination)):
                    this_motif_adj[first_ctr][second_ctr] = network.adjacency[first_node][second_node]
            
            this_motif = Motif(this_motif_adj)

            if this_motif.is_connected():                
                truth = [this_motif == old_motif[0] for old_motif in motif_list]
                if (any(truth) == True):
                    index = truth.index(True)
                    motif_list[index][1] = motif_list[index][1]+1
                elif (all(truth) == False) or (len(truth)==0):
                    motif_list.append((this_motif,1))
                else:
                    print "There has been a problem while extracting Motifs"
                    break
            
        return motif_list
