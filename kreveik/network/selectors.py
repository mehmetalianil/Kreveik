"""
In this module, the selectors for the GA elements, networks are defined. A selector returns True
or False due to whether a particular element is eligible for mutation or not. 
"""

import math
import numpy as num
import kreveik.classes as classes
import kreveik.genetic as genetic
import logging

def hard_threshold(network,**kwargs):
    if not ( kwargs['threshold'] ):
        logging.error("The hard_threshold Selector needs a threshold parameter to work.")
        return None
    if network.score < kwargs['threshold']:
        return True
    else:
        return False
    
def logistic(network,**kwargs):
    if not ( kwargs['angle'] ) or not(kwargs['midpoint']):
        logging.error("The logistic Selector needs angle and midpoint parameters to work.")
        return None
    angle = kwargs['angle']
    midpoint = kwargs['midpoint']
    prob = 1-(1/(1+math.exp(-angle*(network.score-midpoint))))
    if prob < num.random.random():
        return True
    else:
        return False

