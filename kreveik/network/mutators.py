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

def degree_preserving_mutation(network, max = 0, def_mutation = point_mutate_adj):
    """
    A mutation that preserves the degree of the network in concern.
    """
      
    adj = network.adjacency
    if max == 0:
        max = 10*len(adj)**2
        
    columns = adj.sum(axis=0)
    rows = adj.sum(axis=1)
    colsnotzero = num.where([item == 0 for item in columns],False)
    rowsnotzero = num.where([item == 0 for item in rows],False)
    #if all columns are zero or all rows are zero we can't proceed
    if len(colsnotzero) != 0 and len(rowsnotzero) != 0:
        for i in xrange(max):
            randomrow = rowsnotzero(num.random.randint(len(colsnotzero)))
            randomcol = colsnotzero(num.random.randint(len(rowsnotzero)))
            boolean = adj[randomrow,randomcol]
            row = adj[randomrow,:]
            col = adj[:,randomcol]
            colitemsnot = num.where([col == boolean],False)
            rowitemsnot = num.where([row == boolean],False)
            randomrowitem = rowitemsnot(num.random.randint(len(colitemsnot)))
            randomcolitem = colitemsnot(num.random.randint(len(colitemsnot)))
            if adj(randomrowitem,randomcolitem) == boolean:
                adj[randomrowitem,randomcolitem] = not(adj[randomrowitem,randomcolitem])
                adj[randomcolitem,randomcol] = not(adj[randomcolitem,randomcol])
                adj[randomrow,randomrowitem] = not(adj[randomrow,randomrowitem])
                adj[randomrow,randomcol] = not(adj[randomrow,randomcol])
        logging.info("This network "+str(network)+"is unlikely to have a degree preserving\
                      mutation. The default mutation is applied.")
        def_mutation(network)  
    else:
        logging.info("Network "+str(network)+" evolved such that there's no connection left.\
                      The default mutation is applied.")
        def_mutation(network)
        