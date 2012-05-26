from kreveik import *
import logging
import numpy as num
import shelve
logging.basicConfig(level=logging.INFO)

petri = classes.Family()
motiflist = []
scores = []
degrees = []
allmotifs = network.motif.all_conn_motifs(3)

for i in xrange(200):
    a = network.generators.random(7, network.boolfuncs.xor_masking_C,
                                     probability=(0.2,0.5,0.5),
                                     connected=True)
    petri.add(a)
    

petri.scorer = network.scorers.sum_scorer_f
petri.selector = network.selectors.hard_threshold_with_probability
petri.mutator = network.mutators.degree_preserving_mutation
petri.killer = family.killer.random_killer
petri.populate_equilibria()

    
for i in xrange(100):
    for j in xrange(20):
        print "("+str(i)+"/100) ("+str(j)+"/20)"
        kwargs = {'motiflist':allmotifs[:],'prob':0.4,'threshold':2}
        genetic.genetic_iteration(petri,**kwargs)
        degrees.append(num.mean([element.outdegree() for element in petri]))
        scores.append(num.mean([network.score for network in petri]))
    motiflist.append(family.motif_freqs(petri, 3, **kwargs))
    theshelve = shelve.open("backup"+str(i)+"of100.dat")
    theshelve["petri"] = petri
    theshelve["scores"] = scores
    theshelve["degrees"] = degrees
    theshelve["motiflist"] = motiflist
    theshelve.close()
