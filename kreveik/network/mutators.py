import numpy as num
import logging

def point_mutate_adj(network):
    '''
    Will result in a series of implicit point mutation of the adjacency matrix
    '''

    logging.info("Network "+str(network)+" is mutated")
    num.random.seed()
    random_i = num.random.randint(0, network.n_nodes)
    random_j = num.random.randint(0, network.n_nodes)
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

def degree_preserving_mutation(network, maximum = 0, def_mutation = False):
    """
    A mutation that preserves the degree of the network in concern.
    """
      
    adj = network.adjacency
    if maximum == 0:
        maximum = 10*len(adj)**2
    columns = adj.sum(axis=0)
    rows = adj.sum(axis=1)
    colsnotzero = num.where(columns != 0)[0]
    rowsnotzero = num.where(rows != 0)[0]
    #if all columns are zero or all rows are zero we can't proceed
    
    if len(colsnotzero) > 1 and len(rowsnotzero) > 1:
        for cntr in xrange(maximum):
            
            randomrow = rowsnotzero[num.random.randint(len(rowsnotzero))]
            randomcol = colsnotzero[num.random.randint(len(colsnotzero))]
            boolean = adj[randomrow][randomcol]
            row = adj[randomrow,:]
            col = adj[:,randomcol]
            colitemsnot = num.where(col != boolean)[0]
            rowitemsnot = num.where(row != boolean)[0]
            randomrowitem = rowitemsnot[num.random.randint(len(rowitemsnot))]
            randomcolitem = colitemsnot[num.random.randint(len(colitemsnot))]
            
            if adj[randomrowitem][randomcolitem] == boolean:
                
                adj[randomrowitem,randomcolitem] = not(adj[randomrowitem,randomcolitem])
                adj[randomcolitem,randomcol] = not(adj[randomcolitem,randomcol])
                adj[randomrow,randomrowitem] = not(adj[randomrow,randomrowitem])
                adj[randomrow,randomcol] = not(adj[randomrow,randomcol])
                return network
            
        logging.info("This network "+str(network)+"is unlikely to have a degree preserving\
                      mutation. The network is returned as is.")
    else:
        logging.info("Network "+str(network)+" evolved such that there's no connection left.\
                      The network is returned as is.")
               