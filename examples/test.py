from kreveik import *
import copy
import logging
import numpy as num
logging.basicConfig(level=logging.INFO)

# Create a family of 100 individuals with 10 nodes.
petri = classes.Family()
for i in xrange(100):
    a = network.generators.random(5, network.boolfuncs.xor_masking_C, 
                                     network.scorers.orbit_length_sum_f,
                                     probability=(1.0/5,0.5,0.5))
    petri.add(a)

# Extract the 3-motifs of these individuals.
motiflist = []
scores = []

allmotifs = network.all_conn_motifs(3)
kwargs = {"motiflist":allmotifs}
# motifs will be a  list of [motif,freq] list doublets.

petri.scorer = network.scorers.orbit_length_sum_f
petri.mutator = network.mutators.point_mutate_adj
petri.killer = family.killer.random_killer
petri.selector = network.selectors.hard_threshold
petri.populate_equilibria()


for i in xrange(100):
    motiflist.append(family.motif_freqs(petri, 3, **kwargs))
    for j in xrange(1):
        print petri.network_list
        genetic.genetic_iteration(petri,**{'threshold':num.array([network.score for network in petri]).mean()}) 
        print "mean score:"
        print num.array([network.score for network in petri]).mean()
        scores.append(num.array([network.score for network in petri]).mean())
    
    