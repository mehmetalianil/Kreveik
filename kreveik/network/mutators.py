import numpy as num
import logging
from kreveik import *

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
    
def degree_and_connectivity_preserving_mutation(network, maximum = 0, def_mutation = False):
    """
    A mutation that preserves the degree of the network in concern.
    """
    adj = network.adjacency
    logging.debug( "Adjacency Matrix:")
    logging.debug( adj)
    if maximum == 0:
        maximum = 10*len(adj)**2
    columns = adj.sum(axis=0)
    rows = adj.sum(axis=1)
    colsnotzero = num.where(columns != 0)[0]
    rowsnotzero = num.where(rows != 0)[0]
    #if all columns are zero or all rows are zero we can't proceed
    
    if len(colsnotzero) > 0 and len(rowsnotzero) > 0:
        for cntr in xrange(maximum):
            logging.debug( "    Initiating...")
            randomrow = rowsnotzero[num.random.randint(len(rowsnotzero))]
            randomcol = colsnotzero[num.random.randint(len(colsnotzero))]
            logging.debug("Selected item:")
            logging.debug((randomrow,randomcol))
            adj_debug = num.array(adj[:],dtype=str)
            logging.debug(adj_debug)
            adj_debug[randomrow][randomcol] = "1"
            boolean = adj[randomrow][randomcol]
            row = adj[randomrow,:]
            col = adj[:,randomcol]
            colitemsnot = num.where(col != boolean)[0]
            rowitemsnot = num.where(row != boolean)[0]
            randomrowitem = rowitemsnot[num.random.randint(len(rowitemsnot))]
            randomcolitem = colitemsnot[num.random.randint(len(colitemsnot))]
            adj_debug[randomcolitem,randomcol]="2"
            adj_debug[randomrow,randomrowitem]="3"
            adj_debug[randomcolitem,randomrowitem]="4"
            logging.debug(adj_debug)
            if adj[randomcolitem][randomrowitem] == boolean:  
                logging.debug("Success!"  )            
                adj[randomcolitem,randomrowitem] = not(adj[randomcolitem,randomrowitem])
                adj[randomcolitem,randomcol] = not(adj[randomcolitem,randomcol])
                adj[randomrow,randomrowitem] = not(adj[randomrow,randomrowitem])
                adj[randomrow,randomcol] = not(adj[randomrow,randomcol])
                logging.debug("New Network:")
                logging.debug( num.array(adj[:],dtype=str))
                if network.is_connected():
                    return network
            
        logging.info("This network "+str(network)+"is unlikely to have a degree preserving\
                      mutation. The network is returned as is.")
    else:
        logging.info("Network "+str(network)+" evolved such that there's no connection left.\
                      The network is returned as is.")

def degree_preserving_mutation(network, maximum = 0, def_mutation = False):
    """
    A mutation that preserves the degree of the network in concern.
    """
    adj = network.adjacency
    logging.debug( "Adjacency Matrix:")
    logging.debug( adj)
    if maximum == 0:
        maximum = 10*len(adj)**2
    columns = adj.sum(axis=0)
    rows = adj.sum(axis=1)
    colsnotzero = num.where(columns != 0)[0]
    rowsnotzero = num.where(rows != 0)[0]
    #if all columns are zero or all rows are zero we can't proceed
    
    if len(colsnotzero) > 0 and len(rowsnotzero) > 0:
        for cntr in xrange(maximum):
            logging.debug( "    Initiating...")
            randomrow = rowsnotzero[num.random.randint(len(rowsnotzero))]
            randomcol = colsnotzero[num.random.randint(len(colsnotzero))]
            logging.debug("Selected item:")
            logging.debug((randomrow,randomcol))
            adj_debug = num.array(adj[:],dtype=str)
            logging.debug(adj_debug)
            adj_debug[randomrow][randomcol] = "1"
            boolean = adj[randomrow][randomcol]
            row = adj[randomrow,:]
            col = adj[:,randomcol]
            colitemsnot = num.where(col != boolean)[0]
            rowitemsnot = num.where(row != boolean)[0]
            randomrowitem = rowitemsnot[num.random.randint(len(rowitemsnot))]
            randomcolitem = colitemsnot[num.random.randint(len(colitemsnot))]
            adj_debug[randomcolitem,randomcol]="2"
            adj_debug[randomrow,randomrowitem]="3"
            adj_debug[randomcolitem,randomrowitem]="4"
            logging.debug(adj_debug)
            if adj[randomcolitem][randomrowitem] == boolean:  
                logging.debug("Success!"  )            
                adj[randomcolitem,randomrowitem] = not(adj[randomcolitem,randomrowitem])
                adj[randomcolitem,randomcol] = not(adj[randomcolitem,randomcol])
                adj[randomrow,randomrowitem] = not(adj[randomrow,randomrowitem])
                adj[randomrow,randomcol] = not(adj[randomrow,randomcol])
                logging.debug("New Network:")
                logging.debug( num.array(adj[:],dtype=str))
                return network
            
        logging.info("This network "+str(network)+"is unlikely to have a degree preserving\
                      mutation. The network is returned as is.")
    else:
        logging.info("Network "+str(network)+" evolved such that there's no connection left.\
                      The network is returned as is.")
               