import generators
import mutators
import scorers
import selectors
import boolfuncs


def global_clustering_out(network):
    """
    Returns the global clustering coefficient for output connections for every single node 
    """
    local_clustering_out(network).mean()

def global_clustering_in(network):
    """
    Returns the global clustering coefficient for input connections for every single node 
    """
    local_clustering_in(network).mean()
                