import numpy as num
import itertools
import kreveik.classes as classes
import logging
from kreveik import * 
import generators
import mutators
import scorers
import selectors
import boolfuncs

def all_conn_motifs(nodes):
    """Returns a list of all connected motifs for a degree.
    """
    motiflist = []
    degree = nodes**2
    for number in xrange(2**degree):
        linear = num.array([int(item) for item in [False]*
                   (degree-len(list(bin(number)[2:])))+list(bin(number)[2:])],dtype=bool)
        motifadj = num.reshape(linear,(nodes,nodes))
        motif = classes.Motif(motifadj)
        if motif.is_connected() and not(any([motif==motiffromlist[0] for
                                              motiffromlist in motiflist])):
                motiflist.append([motif,0])
    return motiflist

    
def motif_freqs (network,degree,**kwargs):
    """
    Returns a list of motifs for a given network
    """

    logging.info("Extracting "+str(degree)+" motifs of network "+str(network))
    all_combinations = itertools.combinations(range(len(network.adjacency)),degree)
    
    
    
    if 'motiflist' in kwargs:
        motif_list = kwargs['motiflist']
    else:
        logging.info("Creating all possible motifs of node count "+str(degree)+".")
        allmotifs = all_conn_motifs(degree)
        motif_list = allmotifs
    
    logging.info("Extracting motifs from all possible "+str(degree)+" node combinations of the network.")
    
    for combination in all_combinations:
        logging.debug("Motif Permutation:"+str(list(combination)))
        
        this_motif_adj = num.zeros((degree,degree))
        for (first_ctr,first_node) in enumerate(list(combination)):
            for (second_ctr,second_node) in enumerate(list(combination)):
                this_motif_adj[first_ctr][second_ctr] = network.adjacency[first_node][second_node]
        
        this_motif = classes.Motif(this_motif_adj)

        if this_motif.is_connected():
            truth = [this_motif == motif_vec[0]for motif_vec in motif_list]
            if (any(truth) == True):
                index = truth.index(True)
                motif_list[index][1] = motif_list[index][1]+1
            elif (all(truth) == False) or (len(truth)==0):
                motif_list.append([this_motif,1])
            else:
                logging.error("There has been a problem while extracting Motifs")
                break
        
    logging.info("Extraction done!")
    return motif_list
