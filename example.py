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
    
def main():   
    petri = [None]*100
    probelist = [None]*100

    for prob_ctr in xrange(100):
        petri[prob_ctr] = classes.Family()
        probelist[prob_ctr]  = probes.eq_score_probe()
        print "Probability : "+str(prob_ctr/99.0) 
        for indiv in xrange(40):
            petri[prob_ctr].add_to_family(classes.generate_random(7,
                                                scorers.sum_scorer,
                                                boolfuncs.xor_masking,
                                                probability = (prob_ctr/99.0,0.5,0.5)))
            
        petri[prob_ctr].attach(probelist[prob_ctr])    
        petri[prob_ctr].populate_equilibria_in_family()
        
if __name__ == '__main__':
    pass