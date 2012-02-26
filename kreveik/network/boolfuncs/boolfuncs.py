'''
Created on Sep 8, 2011
'''

__author__ = "Mehmet Ali Anil"
__copyright__ = ""
__credits__ = ["Mehmet Ali Anil"]
__license__ = ""
__version__ = "0.0.5"
__maintainer__ = "Mehmet Ali Anil"
__email__ = "anilm@itu.edu.tr"
__status__ = "Production"
        
import numpy as num
import logging
import boolfuncs_c

def xor_masking(network,state):
    """
   
    """
    
    state = num.array(state,dtype=bool)
    newstate = num.array([None]*network.n_nodes)
    
    for i in xrange(network.n_nodes):
        #    Detect all nodes that have an incoming connection
        
        nonzero_of_adj = network.adjacency[i,].nonzero()[0]
        
        #    Reduce the boolean function and the state to a boolean function
        #     and state concerning only the incoming connections.
        
        short_mask = network.mask[i,].take(nonzero_of_adj)
        short_state = state.take(nonzero_of_adj)
    
        #    Two vectors are XOR' d element wise, and is summed in modulo 2
        #    This corresponds to i th node operating its boolean function over the same
        #    state vector.
        
        newstate[i] = (num.logical_xor(short_mask,short_state).sum()<len(short_state)/2.0)
        
    try:
        return newstate
    except:
        logging.error("XOR masking failed in network")
        logging.error("Printing id:")
        logging.error(id(network))
        return False



    
def and_masking(network,state):
    """

    """
    state = num.array(state)
    newstate=num.zeros(network.n_nodes)
    for i in range(0,network.n_nodes):
        nonzero_of_adj = network.adjacency[i,].nonzero()[0]
        short_mask = network.mask[i,].take(nonzero_of_adj)
        short_state =state.take(nonzero_of_adj)
        sum_of_bool = num.logical_and(short_mask,short_state).sum()
        newstate[i]=(len(short_state)/2.0) < sum_of_bool
    try:
        return newstate
    except:
        logging.error("AND masking failed in network")
        logging.error("Printing id:")
        logging.error(id(network))
        return False
    
def or_masking(network,state):
    """

    """
    
    newstate=num.zeros(network.n_nodes)
    for i in range(0,network.n_nodes):
        nonzero_of_adj = network.adjacency[i,].nonzero()[0]
        short_mask = network.mask[i,].take(nonzero_of_adj)
        short_state = network.state[-1].take(nonzero_of_adj)
        sum_of_bool = num.logical_or(short_mask,short_state).sum()
        newstate[i]=(len(short_state)/2.0) < sum_of_bool
    try:
        return newstate
    except:
        logging.error("OR masking failed in network")
        logging.error("Printing id:")
        logging.error(id(network))
        return False
    
def xor_masking_C(network,state):

    newstate = boolfuncs_c.xor_masking_c(network.adjacency,network.mask,state)
    return newstate

def or_masking_C(network,state):

    newstate = boolfuncs_c.or_masking_c(network.adjacency,network.mask,state)
    return newstate

def and_masking_C(network,state):

    newstate = boolfuncs_c.and_masking_c(network.adjacency,network.mask,state)
    return newstate
