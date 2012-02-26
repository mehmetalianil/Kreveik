'''
Created on Mar 8, 2011

@author: Mehmet Ali Anil
'''

from kreveik import * 
import numpy as num
import matplotlib.pyplot as plt
import copy
from kreveik import network


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
    motifbox = [None]*50
    scorebox = [None]*50
    for network_number in xrange(40):
        petri.add_to_family(classes.generate_random(7,
    	                                    network.scorers.orbit_length_sum_f,
    	                                    network.boolfuncs.xor_masking_C,
    	                                    probability = (0.5,0.5,0.5))) 
	                                    
    for i in xrange(50):
        print "Genetic Iteration #"+str(i)
        motifbox[i] = petri.motif_freqs(3)
        scorebox[i] = petri.scores
        petri.genetic_iteration(petri.scores.mean(),mutant_recipe=('Connections',1))
        
        
    #petri[counter].populate_equilibria_in_family()
    #scores[counter] = [network.score for network in petri[counter].network_list]

    
    

    
    
    
        
