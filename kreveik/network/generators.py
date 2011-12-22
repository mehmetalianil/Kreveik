import numpy as num
from kreveik.classes import Network
import logging

def random(n_nodes,function,probability=(0.5,0.5,0.5),connected=False):
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
    state=(num.random.random((1,n_nodes))<probability[1])
    bool_fcn=(num.random.random((n_nodes,n_nodes))<probability[2])
    new_network = Network(adjacency_matrix, bool_fcn, function, state_vec=state)
    
    if connected==False:
        try:
            logging.info("Generating one network of node count "+str(n_nodes))
            return new_network
        
        except ValueError,e:
            z = e
            logging.error("Network is too big to model.")
            print z
            
    elif new_network.is_connected():
        try:
            logging.info("Generating one network of node count "+str(n_nodes))
            return new_network
        
        except ValueError,e:
            z = e
            logging.error("Network is too big to model.")
            print z
    else:
        while not new_network.is_connected():
            num.random.seed()
            adjacency_matrix=(num.random.random((n_nodes,n_nodes))<probability[0])
            state=(num.random.random((1,n_nodes))<probability[1])
            bool_fcn=(num.random.random((n_nodes,n_nodes))<probability[2])
            new_network = Network(adjacency_matrix, bool_fcn, function,state_vec=state)
        
        try:
            logging.info("Generating one network of node count "+str(n_nodes))
            return new_network
        except ValueError,e:
            z = e
            logging.error("Network is too big to model.")
            print z
         
    return new_network