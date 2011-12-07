from kreveik import *
import numpy as num
import copy
import itertools 
import logging

def random_killer(ensemble,times):
    logging.info("Killing "+str(times)+" individuals")
    for i in range(times):
        randomnum = num.random.randint(0,len(ensemble))
        logging.info("("+str(i)+"/"+str(times)+") Killing "+str(ensemble[randomnum]))
        ensemble.remove(randomnum)
    
def qualified_killer(ensemble,**kwargs):
    pass

def underachiever_killer(ensemble,**kwargs):
    pass

    