import classes
import numpy as num
import copy
import itertools 
import logging
import probes


def random_killer(ensemble):
    randomnum = num.random.randint(0,len(ensemble))
    ensemble.remove(randomnum)
    
def qualified_killer(ensemble,**kwargs):
    pass

def underachiever_killer(ensemble,**kwargs):
    pass

    