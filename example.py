from kreveik import *
import logging
import numpy as num
logging.basicConfig(level=logging.INFO)

petri = classes.Family()
motiflist = []
scores = []
degrees = []
allmotifs = network.all_conn_motifs(3)

for i in xrange(200):
    a = network.generators.random(7, network.boolfuncs.xor_masking_C,
                                     probability=(0.2,0.5,0.5),
                                     connected=True)
    petri.add(a)
    

petri.scorer = network.scorers.sum_scorer_f
petri.selector = network.selectors.hard_threshold_with_probability
petri.mutator = network.mutators.degree_preserving_mutation
petri.killer = family.killer.random_killer


for i in xrange(100):
    print "("+str(i)+"/100)"
    kwargs = {'motiflist':allmotifs[:],'prob':0.2,'threshold':0.01}
    genetic.genetic_iteration(petri,**kwargs)
    motiflist.append(family.motif_freqs(petri, 3, **kwargs))
    scores.append(num.mean([network.score for network in petri]))
    degrees.append(num.mean([element.outdegree() for element in petri]))
    print [element.outdegree() for element in petri]
    
