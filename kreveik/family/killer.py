from kreveik import *
import numpy as num
import copy
import itertools 
import logging


def random_killer(ensemble,times):
    for i in xrange(times):
        randomnum = num.random.randint(0,len(ensemble))
        ensemble.remove(randomnum)
    
def qualified_killer(ensemble,**kwargs):
    pass

def underachiever_killer(ensemble,**kwargs):
    pass

    