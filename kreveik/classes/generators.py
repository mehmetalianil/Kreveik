import numpy as num
import matplotlib.pyplot as plt
import copy
import networkx as nx
from ..classes import *

print_enable=True

def generate_random(n_nodes,scorer,function,probability=(0.5,0.5,0.5)):
    '''
    Generates and returns a random network with a random initial conditions.
    The adjacency matrix, initial state, boolean function are populated with 
    1's and 0's with probabilities of 0.5.
    
    Input Variables
    n_nodes -> Number of nodes in the system. A value of 2 to 8 will generate a 
    network with manageable size and complexity.
    probability -> The probability of having a connection in any two nodes. 
    A smaller value will decrease complexity and clustering coefficient.  
    scorer -> a function for the type network
    '''
    num.random.seed()
    adjacency_matrix=(num.random.random((n_nodes,n_nodes))<probability[0])
    #    First state of the system is determined
    state=(num.random.random((1,n_nodes))<probability[1])
    bool_fcn=(num.random.random((n_nodes,n_nodes))<probability[2])

    try:
        return Network(adjacency_matrix, bool_fcn, scorer,function,state_vec=state)
        
    except ValueError,e:
        z = e
        print "Network is too big to model."
        print z
    
    return 