import numpy as num
import itertools
import logging
import kreveik
import kreveik.classes as classes
import killer



def motif_freqs(family,degree, sorting=False, **kwargs):
    """
    Returns a list of motifs of the family.
    """
    from kreveik import network
    import copy 
    
    if  'motiflist' in kwargs:
        returned_motifs = copy.deepcopy(kwargs['motiflist'])
    else:
        returned_motifs = network.all_conn_motifs(degree)[:]

    logging.info("Computing motif frequencies of the family")
    for networkf in family:
        returned_motifs = network.motif_freqs(networkf, degree, motiflist=returned_motifs)           
        
    if sorting:
        return  sorted (returned_motifs, key = lambda returned_motifs:returned_motifs[1] , reverse = True)
    else:
        return returned_motifs

def mean_connectivity(family):
    """
    The mean connectivity of a Family of networks is returned.
    """
    [network.network for network in family]
    
def populate_equilibria(family,jobserver=None):
    """
    Wrapper for family method classes.family.populate_equilibria
    Rewritten for parallel integraton
    """
    import pp,logging
    import numpy as num
    
    if jobserver == None:
        logging.info("There isn't any jobserver available, Computing unicore.")
        family.populate_equilibria()
        return family
    else:
        logging.info("There is a jobserver supplied. Will try parallel.")
        n_network = len(family.network_list)
        active_nodes = jobserver.get_active_nodes()
        
        for node in active_nodes:
            logging.info("There are "+str(active_nodes[node])+" cores at "+str(node))
        
        
        if len(active_nodes) == 1:
            # this means that there is only one computer with numerous cores.
            number_of_cores = active_nodes['local']
            networks = family.network_list
            network_batches = range(number_of_cores)
            for counter in network_batches:
                network_batches[counter] = networks[counter*n_network/number_of_cores:
                                     (counter+1)*n_network/number_of_cores]
            print "network batches:"
            print network_batches
            job_batches  = [jobserver.submit(kreveik.network.populate_equilibria,
                                             (network_batch,),(),
                                             ("numpy as num","kreveik.probes as probes"))
                            
                            # I omitted a callback function here !!
                            for network_batch in network_batches]
            
            returned_networks = [job() for job in job_batches]
            new_network_list = [network for networks in returned_networks for network in networks]
            # flattens the list fast
            family.network_list = new_network_list
            return new_network_list
                             
        else:
            # this means that there are other computers, we can use a master-slave 
            # configuration
            print "Testing!!"
        
        
        
        
    
    