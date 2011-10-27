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
    
    petri=[None]*101
    scores=[None]*101
    
    for counter in xrange(101):
        print "Family #" +str(counter)
        petri[counter] = classes.Family()
        prob = counter/100.0
        for network_number in xrange(100):
            petri[counter].add_to_family(classes.generate_random(7,
        	                                    scorers.orbit_length_sum,
        	                                    boolfuncs.xor_masking_C,
        	                                    probability = (prob,0.5,0.5))) 
    	                                    
        petri[counter].populate_equilibria_in_family()
        scores[counter] = [network.score for network in petri[counter].network_list]
   
    
    

    
    
    
        
