from kreveik import *
import logging
logging.basicConfig(level=logging.INFO)

# Create a family of 100 individuals with 10 nodes.
petri = classes.Family()
for i in xrange(10):
    a = network.generators.random(7, network.boolfuncs.xor_masking_C, 
                                     network.scorers.orbit_length_sum_f,
                                     probability=(1.0/7,0.5,0.5))
    petri.add(a)

# Extract the 3-motifs of these individuals.

motiflist = family.motif_freqs(petri, 3)
    
# motifs will be a  list of [motif,freq] list doublets.

petri.scorer = network.scorers.orbit_length_sum_f
petri.mutator = network.mutators.point_mutate_adj
petri.killer = family.killer.random_killer
petri.selector = network.selectors.hard_threshold

genetic.genetic_iteration(petri,**{'threshold':1}) 
