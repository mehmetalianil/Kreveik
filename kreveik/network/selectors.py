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
    if not('threshold' in  kwargs):
        logging.error("The hard_threshold Selector needs a threshold parameter to work.")
        return None
    if network.score < kwargs['threshold']:
        logging.info("score = "+str(network.score)+" < "+str(kwargs['threshold'])+" = threshold.")
        return True
    elif network.score == kwargs['threshold']:
        logging.info("score = "+str(network.score)+" = "+str(kwargs['threshold'])+" = threshold.")
        if num.random.randint(0,2) == 1:
            return True
        else:
            return False
    else:
        return False
def hard_threshold_with_probability(network,**kwargs):
    if not('threshold' in kwargs):
        logging.error("The hard_threshold Selector needs a threshold parameter to work.")
        return None
    if not('prob' in kwargs):
        logging.error("The hard_threshold Selector needs a prob parameter to work.")
        return None
    
    if network.score < kwargs['threshold']:
        logging.debug("score = "+str(network.score)+" < "+str(kwargs['threshold'])+" = threshold.")
        if num.random.random() < kwargs['prob']:
            return True
        else:
            return False
    elif network.score == kwargs['threshold']:
        logging.debug("score = "+str(network.score)+" = "+str(kwargs['threshold'])+" = threshold.")
        if num.random.randint(0,2) == 1:
            return True
        else:
            return False
    else:
        return False
    
def logistic(network,**kwargs):
    if not ('angle' in kwargs) or not('midpoint' in kwargs):
        logging.error("The logistic Selector needs angle and midpoint parameters to work.")
        return None
    angle = kwargs['angle']
    midpoint = kwargs['midpoint']
    prob = 1-(1/(1+math.exp(-angle*(network.score-midpoint))))
    if prob < num.random.random():
        return True
    else:
        return False

