'''
Created on Mar 8, 2011

@author: Mehmet Ali Anil
'''

from kreveik import * 
import numpy as num
import matplotlib.pyplot as plt
import copy



__author__ = "Mehmet Ali Anil"
__copyright__ = ""
__credits__ = ["Mehmet Ali Anil"]
__license__ = ""
__version__ = "0.0.5"
__maintainer__ = "Mehmet Ali Anil"
__email__ = "anilm@itu.edu.tr"
__status__ = "Production"

        
if __name__ == '__main__':
    petri = classes.Family()
    petri2 = classes.Family()
    
    for counter in xrange(100):
        petri.add_to_family(classes.generate_random(7,
    	                                    scorers.sum_scorer,
    	                                    boolfuncs.xor_masking,
    	                                    probability = (0.5,0.5,0.5))) 
   
    prb_petri_mean_score = probes.family_mean_score_probe()
    #prb_petri2_mean_score = probes.family_mean_score_probe()
    petri.attach(prb_petri_mean_score)
    #petri2.attach(prb_petri2_mean_score)
    prb_petri_motifs= probes.motif_family_probe(3,(0,100))
    #prb_petri2_motifs = probes.motif_network_probe(3)
    petri.attach(prb_petri_motifs)
    #petri2.network_list[-1].attach(prb_petri2_motifs)
    
    for ga_ctr in xrange(100):
        petri.genetic_iteration(petri.scores.mean())
        #petri2.genetic_iteration(petri.scores.mean())
    
    
    
        
