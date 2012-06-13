
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

import logging
import numpy as num
import kreveik


def all_conn_motifs(nodes):
    """
    Returns a list of all connected motifs for a degree.
    
    This function takes every possible (fully connected) configuration of a graph with n nodes.
    And lists them as a list of all possible motifs. 
    
    Input Arguments:
    ---------------
    
    nodes
        The number of nodes of the motifs that will be generated.
    """
    logging.info("Returning all connected motifs with "+str(nodes)+" nodes")
    motiflist = []
    degree = nodes**2
    for number in xrange(2**degree):
        linear = num.array([int(item) for item in [False]*
                   (degree-len(list(bin(number)[2:])))+list(bin(number)[2:])],dtype=bool)
        motifadj = num.reshape(linear,(nodes,nodes))
        motif = kreveik.classes.Motif(motifadj)
        if motif.is_connected() and not(any([motif==motiffromlist[0] for
                                              motiffromlist in motiflist])):
                motiflist.append([motif,0])
    return motiflist

def exclusive_conn_motifs(nodes):
    """
    Returns a list of connected motifs for a degree, excluding self adjacency of the nodes.
    
    This function takes exclusive configurations of a graph with n nodes.
    And lists them as a list of possible motifs. 
    
    Input Arguments:
    ---------------
    
    nodes
        The number of nodes of the motifs that will be generated.
    """
    logging.info("Returning exclusive connected motifs with "+str(nodes)+" nodes")
    exclusive_list = []
    allmotifs = all_conn_motifs(nodes)[:]
    for i in range(len(allmotifs)):
        count = 0
        for j in range(nodes):
            x = allmotifs[i][0].adjacency[j][j]
            if (x == False):                
                count = count + 1
        if (count == nodes):
            exclusive_list.append([allmotifs[i][0],0])
    return exclusive_list
    
def node_duplication(motif):
    #TODO
    """
    Duplicates every node in a motif for a given number of times,
    generates a new motif for every node duplication, and returns
    a list of all the generated motifs.
    """
    motiflist=[]
    new_adjacency=motif.adjacency
    for i in range(len(motif.adjacency)):
        in_going=motif.adjacency[i][:]          
        out_going=motif.adjacency[:][i]
#        for j in range(number):
        new_adjacency = num.append(new_adjacency, in_going)
        transposed_adjacency = num.append(num.transpose(new_adjacency), out_going)
        new_adjacency = num.transpose(transposed_adjacency)
        motif = kreveik.classes.Motif(new_adjacency)
        motiflist.append(motif)
    return motiflist

def motif_freqs (network,degree,exclusive = False,**kwargs):
    """
    Returns a list of motifs for a given network
    
    This function takes every possible combinations of nodes counting degree, out of all
    nodes of the network provided, and counts them in a list of all motifs, by default. If
    the argument exclusive is set True, it takes only exclusive motifs (excluding self 
    adjacencies of the nodes) into account.  
    
    Args:
    ----
        network: the network which motif frequencies will be found.
        degree: the number of nodes of the motifs that will be searched in the network.
        exclusive: False by default. If set True, the search will be limited to exclusive motifs.
        motiflist: an optional argument in which if supplied, the search will be limited to
        motifs in that list.
        accumulate: if True, will accumulate motifs omitted in the motiflist provided.
        
    Returns:
    -------
    A numpy array of [Motif object , number of occurences], an N x 2 array. 
        
    """
    import itertools
    
    logging.info("Extracting "+str(degree)+" motifs of network "+str(network))
    all_combinations = itertools.combinations(range(len(network.adjacency)),degree)
    
    if 'accumulate' in kwargs:
        accumulate = kwargs['accumulate'] 
    else: 
        accumulate = False
        
    if 'motiflist' in kwargs:
        allmotifs = kwargs['motiflist'][:]
        motif_list = allmotifs[:]
        if len(motif_list[0]) == 1:
            # if only a list of motifs are presented, not a list and numbers.
            motif_list = num.array([[motif,0] for motif in motif_list])
    else:
        logging.info("Creating all possible motifs of node count "+str(degree)+".")
        if (exclusive == True):
            motif_list = exclusive_conn_motifs(degree)[:]
        else:
            motif_list = all_conn_motifs(degree)[:]
        
    logging.info("Extracting motifs from all possible "+str(degree)+" node combinations of the network.")
    
    for combination in all_combinations:
        logging.debug("Motif Permutation:"+str(list(combination)))
        
        this_motif_adj = num.zeros((degree,degree), dtype = bool)
        for (first_ctr,first_node) in enumerate(list(combination)):            
            for (second_ctr,second_node) in enumerate(list(combination)):
                if (exclusive == True) and (first_ctr == second_ctr):
                    this_motif_adj[first_ctr][second_ctr] = 0
                else:                    
                    this_motif_adj[first_ctr][second_ctr] = network.adjacency[first_node][second_node]
        
        this_motif = kreveik.classes.Motif(this_motif_adj)
        logging.debug("Motif Adjacency:")
        logging.debug(list(combination))
        logging.debug(str(this_motif_adj))
        if this_motif.is_connected():
            truth = [this_motif == motif_vec[0] for motif_vec in motif_list]
            if (any(truth) == True):
                index = truth.index(True)
                motif_list[index][1] = motif_list[index][1]+1
            
            elif accumulate: 
                if (all(truth) == False):
                    logging.debug("Added new motif,"+str(id(this_motif)))
                    motif_list.append([this_motif,1])
        
    logging.info("Extraction done!")
    return motif_list

def relative_motif_freqs (network,degree,**kwargs):
    """
    Returns a list of motifs and their number of occurrences as a fraction of the total
    number of occurrences of all the motifs in the list, for a given network.
    
    Args:
    ----
        network: the network which motif frequencies will be found.
        degree: the number of nodes of the motifs that will be searched in the network.
        motiflist: an optional argument in which if supplied, the search will be limited to
        motifs in that list.
        
    Returns:
    -------
    A numpy array of [Motif object , number of occurrences over total number of occurrences], 
    an N x 2 array. 
        
    """
    if 'motiflist' in kwargs:
        allmotifs = kwargs['motiflist'][:]
        motif_list = allmotifs[:]
    else:
        logging.info("Creating all possible motifs of node count "+str(degree)+".")
        motif_list = all_conn_motifs(degree)[:]
    network_motifs = motif_freqs(network, degree, motiflist=motif_list)[:]
    motif_counts = num.array([[network_motifs[i][1]] for i in range(len(network_motifs))])
    relative_freqs = []
    for i in range(len(network_motifs)):
        relative_freqs.append([network_motifs[i][0], float(network_motifs[i][1])/motif_counts.sum()])
    return num.array(relative_freqs)

__all__ = [motif_freqs, exclusive_conn_motifs, all_conn_motifs, node_duplication, 
           relative_motif_freqs ]