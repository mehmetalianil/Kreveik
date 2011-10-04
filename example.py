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
        
import cProfile
        
if __name__ == '__main__':
    petri = classes.Family()
    petri.add_to_family(classes.generate_random(7,
	                                    scorers.sum_scorer,
	                                    boolfuncs.xor_masking,
	                                    probability = (0.5,0.5,0.5)))
    
