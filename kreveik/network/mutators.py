import numpy as num

def point_mutate_adj(network):
        '''
        Will result in a series of implicit point mutation of the adjacency matrix
        '''

        num.random.seed()
        random_i = num.random.randint(0, network.n_nodes-1)
        random_j = num.random.randint(0, network.n_nodes-1)
        network.adjacency[random_i][random_j] = not(network.adjacency[random_i][random_j])
            
def point_mutate_mask(network):
        '''
        Will result in a series of implicit point mutation of the masks
    '''                        
    
        num.random.seed()
        random_i = num.random.randint(0, network.n_nodes-1)
        random_j = num.random.randint(0, network.n_nodes-1)
        network.mask[random_i][random_j] = not(network.mask[random_i][random_j])