import numpy as num
import itertools
import logging
import kreveik.classes as classes
import killer


def motif_freqs(family,degree, sorted=False, **kwargs):
    """
    Returns a list of motifs of the family.
    """
    from kreveik import network
    
    if  'motiflist' in kwargs:
        allmotifs = kwargs['motiflist']
    else:
        allmotifs = network.all_conn_motifs(degree)
        
    logging.info("Computing motif frequencies of the network")
    
    for networkf in family:
        allmotifs = network.motif_freqs(networkf, degree, motiflist=allmotifs)
    if sorted:
        return  sorted (allmotifs, key = lambda allmotifs:allmotifs[1] , reverse = True)
    else:
        return allmotifs