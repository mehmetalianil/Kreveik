
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
    
__all__= [generators,mutators, scorers,selectors,boolfuncs,motif,
          global_clustering_in, global_clustering_out, local_clustering_out,
          local_clustering_in]
                