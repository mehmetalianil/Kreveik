import numpy as num
import itertools
import logging
import kreveik.classes as classes
import killer


def motif_freqs(family,degree, sorting=False, **kwargs):
    """
    Returns a list of motifs of the family.
    """
    from kreveik import network
    import copy 
    
    if  'motiflist' in kwargs:
        returned_motifs = copy.deepcopy(kwargs['motiflist'])
    else:
        returned_motifs = network.all_conn_motifs(degree)[:]

    logging.info("Computing motif frequencies of the family")
    for networkf in family:
        returned_motifs = network.motif_freqs(networkf, degree, motiflist=returned_motifs)           
        
    if sorting:
        return  sorted (returned_motifs, key = lambda returned_motifs:returned_motifs[1] , reverse = True)
    else:
        return returned_motifs

def mean_connectivity(family):
    """
    The mean connectivity of a Family of networks is returned.
    """
    [network.network for network in family]