
#    Copyright 2012 Mehmet Ali ANIL
#    
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#    
#    http://www.apache.org/licenses/LICENSE-2.0
#    
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""
network package
==============

This package includes functions that concern network-like objects

Modules
-------
boolfuncs: 
    Boolean functions that carry one state of a network to another (propogators).

generators:
    Functions that generate networks. 
    
mutators:
    Functions that mutate functions

scorers:
    Functions that score networks

selectors:
    Functions that select networks genetic elimination
    
motif:
    Functions that concerns networks' motifs.
    
Functions
---------
local_clustering_in:  in- clustering for every node 
local_clustering_out:  out- clustering for every node 
global_clustering_out: returns the mean in-clustering of all nodes
global_clustering_in:  returns the mean out-clustering of all nodes

"""

import generators
import mutators
import scorers
import selectors
import boolfuncs
import motif

def local_clustering_in(network):
    """
    Returns the local clustering coefficient for input connections for every single node 
    """
    import numpy as num
    
    adj = network.adjacency*1-num.diagflat(num.diag(network.adjacency*1))
    returned = num.zeros(len(adj))
    for (counter,row) in enumerate(adj):
        k = row.sum()
        where = num.where(k)[0]
        connections=0.0
        for first in where:
            for second in where:
                if adj(first,second)==1 or adj(second,first)==1:
                    connections += 1.0
        returned[counter] = connections /((k)*(k+1))
    return returned

def local_clustering_out(network):
    """
    Returns the local clustering coefficient for output connections for every single node 
    """
    import numpy as num
    
    adj = num.transpose(network.adjacency*1-num.diagflat(num.diag(network.adjacency*1)))
    returned = num.zeros(len(adj))
    for (counter,row) in enumerate(adj):
        k = row.sum()
        where = num.where(k)[0]
        connections=0.0
        for first in where:
            for second in where:
                if adj(first,second)==1 or adj(second,first)==1:
                    connections += 1.0
        returned[counter] = connections /((k)*(k+1))
    return returned

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
    
def randomize(network, number):
    """
    Randomizes a given network, by generating a given number of networks preserving in and out
    degrees of every node.
    """
    network_list=[]
    network_list.append(network)
    for i in range(number):
        new_network=network_list[i].copy()
        network_list.append(mutators.degree_preserving_mutation(new_network))
    return network_list

def randomize_preserving_total_degree(network, number):
    """
    Randomizes a given network, by generating a given number of networks preserving 
    the total in and out degree of the network.
    """
    
    import numpy as num
    import random
    
    network_list=[]
    new_network=network.copy()
    total_degree = num.sum(network.adjacency*1)
    
    
    for i in range(number):
        j = 0
        new_adjacency = new_network.adjacency - new_network.adjacency
        new_network.adjacency = new_adjacency
        adjacency_sequence = num.ndarray.flatten(new_network.adjacency)
        while j < total_degree:
            index = random.randrange(0, num.square(len(new_network.adjacency)), step=1)
            if adjacency_sequence[index] == 1:
                j = j
            else:
                adjacency_sequence[index] = 1
                j = j + 1
        new_network.adjacency = adjacency_sequence.reshape(7,7)
        network_list.append(new_network.copy())
        
    return network_list

def z_score(network, number, degree, **kwargs):
    """
    """
    import numpy as num
    if 'motiflist' in kwargs:
        allmotifs = kwargs['motiflist'][:]
        motif_list = allmotifs[:]
    else:
        motif_list = motif.all_conn_motifs(degree)[:]
    networks_list = randomize(network, number)
    network_motifs = []
    z_score_list = []
    original_motifs = motif.relative_motif_freqs(network, degree, motiflist=motif_list)
    for networkz in networks_list:
        relative_motifs = motif.relative_motif_freqs(networkz, degree, motiflist=motif_list)
        motif_count = [[relative_motifs[i][1]] for i in range(len(motif_list))]
        network_motifs.append(motif_count)
    for i in range(len(motif_list)):
        z_score_list.append((num.array(original_motifs[i][1])-num.mean(network_motifs, axis=0)[i])/num.std(network_motifs,axis=0)[i])
    return z_score_list
    
__all__= [generators,mutators, scorers,selectors,boolfuncs,motif,
          global_clustering_in, global_clustering_out, local_clustering_out,
          local_clustering_in, randomize]

                
