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
import copy
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
    probelist = [None]*50
    petri2 = genereg.family()
    eq_probe = probes.eq_score_probe()
    for numbertag,network in enumerate(net): 
        net[numbertag] = genereg.generate_random(4,
                                                 scorers.sum_scorer,
                                                 boolfuncs.xor_masking,
                                                 probability = (0.2,0.5,0.5))
        petri2.add_to_family(net[numbertag])
        probelist[numbertag] = copy.copy(eq_probe)
        petri2.network_list[numbertag].attach(probelist[numbertag])
        
    mean_score_1 = probes.mean_score_probe()
    petri2.attach(mean_score_1)  
    
    

