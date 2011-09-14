'''
Created on Mar 8, 2011

@author: Mehmet Ali Anil
'''
import numpy as num
import classes
import matplotlib.pyplot as plt
import scorers
import probes
import copy
import boolfuncs



__author__ = "Mehmet Ali Anil"
__copyright__ = ""
__credits__ = ["Mehmet Ali Anil"]
__license__ = ""
__version__ = "0.0.5"
__maintainer__ = "Mehmet Ali Anil"
__email__ = "anilm@itu.edu.tr"
__status__ = "Production"
        

if __name__ == '__main__':
    petri=[None]*2000
    scores=[None]*2000
    for n in range(2000):
        petri[n] = classes.Family()
        for m in range(10):
            petri[n].add_to_family(classes.generate_random(7,
                                            scorers.sum_scorer,
                                            boolfuncs.xor_masking,
                                            probability = (n/1999.0,0.5,0.5)))
        petri[n].populate_equilibria_in_family()
        scores[n] = petri[n].scores.mean()  
        print scores[n]
    
    

