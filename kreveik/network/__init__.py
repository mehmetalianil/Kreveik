import numpy as num
from mutator import *

def score(network,scorer=None):
    """
    If a scorer is specified, the score of the network calculated with that
    scorer is returned. 
    If scorer is not set, then the network is scored implicitly,
    """
    if scorer == None:
        network.score = network.scorer(network)
    else
        return scorer(network)