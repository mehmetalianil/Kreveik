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

def xor_masking(network,state):
    """
    For a network, every single node is taken, its mask and state vector is clipped.
    They are subject to a boolean operation from numpy libraries.
    Then from the fact that whether the node outputs a number greater than the 
    shortened state vector, the node outputs 1 or 0.
    These values are gathered up and outputted as a new state vector.
    The method can be:
        num.logical_or
        num.logical_and
        num.logical_xor
        num.logical_xnor
        
        or any other function that outputs an integer with an input of two ndarrays.        
    """
    
    state = num.array(state)
    newstate = num.array([None]*network.n_nodes,dtype=bool)
    
    for i in range(0,network.n_nodes):
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
        print "XOR masking failed in network"
        print "Printing id:"
        print id(network)
        return False
    
    
def and_masking(network,state):
    """
    For a network, every single node is taken, its mask and state vector is clipped.
    They are subject to a boolean operation from numpy libraries.
    Then from the fact that whether the node outputs a number greater than the 
    shortened state vector, the node outputs 1 or 0.
    These values are gathered up and outputed as a new state vector.
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
        print "AND masking failed in network"
        print "Printing id:"
        network.print_id()
        return False
    
def or_masking(network,state):
    """
    For a network, every single node is taken, its mask and state vector is clipped.
    They are subject to a boolean operation from numpy libraries.
    Then from the fact that whether the node outputs a number greater than the 
    shortened state vector, the node outputs 1 or 0.
    These values are gathered up and outputted as a new state vector.
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
        print "OR masking failed in network"
        print "Printing id:"
        network.print_id()
        return False

    