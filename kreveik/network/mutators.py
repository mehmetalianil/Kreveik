import numpy as num
import logging

def point_mutate_adj(network):
    '''
    Will result in a series of implicit point mutation of the adjacency matrix
    '''

    logging.info("Network "+str(network)+" is mutated")
    num.random.seed()
    random_i = num.random.randint(0, network.n_nodes)
    print random_i

    random_j = num.random.randint(0, network.n_nodes)
    print random_j
    network.adjacency[random_i][random_j] = not(network.adjacency[random_i][random_j])
        
def point_mutate_mask(network):
    '''
    Will result in a series of implicit point mutation of the masks
    '''                        
    
    logging.info("Network "+str(network)+" is mutated")
    num.random.seed()
    random_i = num.random.randint(0, network.n_nodes)
    random_j = num.random.randint(0, network.n_nodes)
    network.mask[random_i][random_j] = not(network.mask[random_i][random_j])

def degree_preserving_mutation(network):
    """
    A mutation that preserves the degree of the network in concern.
    """
    pass