import numpy as num
import itertools
import kreveik.classes as classes
import logging

    
def motif_freqs (network,degree):
        """
        Returns a list of motifs.
        """
    
        all_combinations = itertools.combinations(range(len(network.adjacency)),degree)
        motif_list = []
        
        for combination in all_combinations:
            logging.info("Motif Permutation:"+str(list(combination)))
            
            this_motif_adj = num.zeros((degree,degree))
            for (first_ctr,first_node) in enumerate(list(combination)):
                for (second_ctr,second_node) in enumerate(list(combination)):
                    this_motif_adj[first_ctr][second_ctr] = network.adjacency[first_node][second_node]
            
            this_motif = classes.Motif(this_motif_adj)

            if this_motif.is_connected():                
                truth = [this_motif == old_motif[0] for old_motif in motif_list]
                if (any(truth) == True):
                    index = truth.index(True)
                    motif_list[index][1] = motif_list[index][1]+1
                elif (all(truth) == False) or (len(truth)==0):
                    motif_list.append((this_motif,1))
                else:
                    logging.error("There has been a problem while extracting Motifs")
                    break
            
        return motif_list
