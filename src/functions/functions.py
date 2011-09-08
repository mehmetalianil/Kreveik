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

def xor_masking_majority(network):
    first_newstate=len(network.state) 
    newstate=num.zeros(network.n_nodes)
    for i in range(0,network.n_nodes):
        #    Detect all nodes that have an incoming connection
        
        nonzero_of_adj = network.adjacency[i,].nonzero()[0]
        
        #    Reduce the boolean function and the state to a boolean function
        #     and state concerning only the incoming connections.
        
        short_mask = network.mask[i,].take(nonzero_of_adj)
        short_state = network.state[first_newstate-1].take(nonzero_of_adj)
    
        #    Two vectors are XOR' d element wise, and is summed in modulo 2
        #    This corresponds to i th node operating its boolean function over the same
        #    state vector.
        sum_of_xor = num.logical_xor(short_mask,short_state).sum()
        newstate[i]=num.int((len(short_state)/2.0) < sum_of_xor)
    try:
        return newstate
    except:
        print "XOR masking failed in network"
        print "Printing id:"
        network.print_id()
        return False