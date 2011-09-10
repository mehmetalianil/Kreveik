'''
Created on Mar 8, 2011

@author: Mehmet Ali Anil
'''
import numpy as num
import genereg
import matplotlib.pyplot as plt
import pickle
import scorers
import probes
import boolfuncs
import cProfile



__author__ = "Mehmet Ali Anil"
__copyright__ = ""
__credits__ = ["Mehmet Ali Anil"]
__license__ = ""
__version__ = "0.0.5"
__maintainer__ = "Mehmet Ali Anil"
__email__ = "anilm@itu.edu.tr"
__status__ = "Production"
        

if __name__ == '__main__':
    net = [None]*50
    petri2 = genereg.family()
    
    for numbertag,network in enumerate(net): 
        net[numbertag] = genereg.generate_random(5,
                                                 scorers.sum_scorer,
                                                 boolfuncs.xor_masking,
                                                 probability = (0.2,0.5,0.5))
        petri2.add_to_family(net[numbertag])
        petri2.attach(probes.mean_score_probe)
        
    

