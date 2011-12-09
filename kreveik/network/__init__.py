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
    logging.info("Returning all connected motifs with "+str(nodes)+" nodes")
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
        allmotifs = kwargs['motiflist'][:]
        motif_list = allmotifs[:]
    else:
        logging.info("Creating all possible motifs of node count "+str(degree)+".")
        motif_list = all_conn_motifs(degree)[:]
        
    logging.info("Extracting motifs from all possible "+str(degree)+" node combinations of the network.")
    
    for combination in all_combinations:
        logging.debug("Motif Permutation:"+str(list(combination)))
        
        this_motif_adj = num.zeros((degree,degree), dtype = bool)
        for (first_ctr,first_node) in enumerate(list(combination)):
            for (second_ctr,second_node) in enumerate(list(combination)):
                this_motif_adj[first_ctr][second_ctr] = network.adjacency[first_node][second_node]
        
        this_motif = classes.Motif(this_motif_adj)
        logging.debug("Motif Adjacency:")
        logging.debug(list(combination))
        logging.debug(str(this_motif_adj))
        if this_motif.is_connected():
            truth = [this_motif == motif_vec[0] for motif_vec in motif_list]
            if (any(truth) == True):
                index = truth.index(True)
                motif_list[index][1] = motif_list[index][1]+1
            elif (all(truth) == False):
                logging.info("")
                motif_list.append([this_motif,1])
            else:
                logging.error("There has been a problem while extracting Motifs")
                break
        
    logging.info("Extraction done!")
    return motif_list

def local_clustering_in(network):
    """
    Returns the local clustering coefficient for input connections for every single node 
    """
    adj = network.adjacency*1-num.diagflat(num.diag(network.adjacency*1))
    returned = num.zeros(len(adj))
    for (counter,row) in enumerate(adj):
        k = row.sum()
        where = num.where(k)[0]
        connections=0.0
        for first in where:
            for second in where:
                if adj(first,second)==1 or adj(second,first)==1:
                    connections += 1.0
        returned[counter] = connections /((k)*(k+1))
    return returned

def local_clustering_out(network):
    """
    Returns the local clustering coefficient for output connections for every single node 
    """
    adj = num.transpose(network.adjacency*1-num.diagflat(num.diag(network.adjacency*1)))
    returned = num.zeros(len(adj))
    for (counter,row) in enumerate(adj):
        k = row.sum()
        where = num.where(k)[0]
        connections=0.0
        for first in where:
            for second in where:
                if adj(first,second)==1 or adj(second,first)==1:
                    connections += 1.0
        returned[counter] = connections /((k)*(k+1))
    return returned

def global_clustering_out(network):
    """
    Returns the global clustering coefficient for output connections for every single node 
    """
    local_clustering_out(network).mean()

def global_clustering_in(network):
    """
    Returns the global clustering coefficient for input connections for every single node 
    """
    local_clustering_in(network).mean()
                