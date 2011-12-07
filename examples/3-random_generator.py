from kreveik import *
import copy
import logging
import numpy as num
logging.basicConfig(level=logging.INFO)

# Create a family of 100 individuals with 10 nodes.
petri = classes.Family()
for i in xrange(10000):
    
    a = network.generators.random(3, network.boolfuncs.xor_masking_C, 
                                     network.scorers.orbit_length_sum_f,
                                     probability=(1.0/3,0.5,0.5),
                                     connected=True)
    petri.add(a)

allmotifs = network.all_conn_motifs(3)

kwargs = {"motiflist":allmotifs[:]}
motiflist = family.motif_freqs(petri, 3, **kwargs)
