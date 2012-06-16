
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
family.motifs module
====================
Houses functions concerning motif extraction from a Family.

Functions
---------
    motif_freqs: extracts motifs and their frequencies.
    exclusive_motif_freqs: WIP
    
"""

def motif_freqs(family,degree, exclusive=False, sorting=False, **kwargs):
    """
    Returns a list of motifs of the family.
    
    Takes every single individual of a family, extracts motif frequencies of every single one
    of them (Check network.motif.motif_freqs() function), accumulating with each individual.
    When supplied with a motiflist, this function only searches for the motifs within the list.
    If there isn't any motiflist supplied, then the function generates all possible motifs with
    a specified number of nodes, and resumes calculation.
    
    Args:
    ----
    
        family: The family in which motif frequencies will be extracted.
        degree: the number of nodes of motifs in question.
        sorting: if True, will sort the returned list of motif frequencies.
        motiflist: an optional argument, that if supplied, the search for motifs will be 
        limited with that particular list. 
    """
    from kreveik import network
    import copy
    import logging
    
    if  'motiflist' in kwargs:
        returned_motifs = copy.deepcopy(kwargs['motiflist'])
    else:
        if(exclusive == True):
            returned_motifs = network.motif.exclusive_conn_motifs(degree)[:]
        else:
            returned_motifs = network.motif.all_conn_motifs(degree)[:]

    logging.info("Computing motif frequencies of the family")
    for networkf in family:
        returned_motifs = network.motif.motif_freqs(networkf, degree, motiflist=returned_motifs)           
        
    if sorting:
        return  sorted (returned_motifs, key = lambda returned_motifs:returned_motifs[1] , reverse = True)
    else:
        return returned_motifs
    
def relative_motif_freqs(network_family, degree, sorting=False, **kwargs):
    """
    """
    from kreveik import network
    import copy
    import logging
    import numpy as num
    
    if  'motiflist' in kwargs:
        returned_motifs = copy.deepcopy(kwargs['motiflist'])
    else:
        returned_motifs = network.motif.all_conn_motifs(degree)[:]
    logging.info("Computing relative motif frequencies of the family")
    family_motifs = motif_freqs(network_family, degree, motiflist=returned_motifs)[:]
    motif_counts = num.array([[family_motifs[i][1]] for i in range(len(family_motifs))])
    relative_freqs = []
    for i in range(len(family_motifs)):
        relative_freqs.append([family_motifs[i][0], float(family_motifs[i][1])/motif_counts.sum()])
    return num.array(relative_freqs)

def exclusive_motif_freqs(family,degree):
    """
    Work in Progress
    """
    from kreveik import network
    import copy
    import logging
    motifs = network.motif.exclusive_conn_motifs(degree)[:]
    for networkf in family:
        logging.info("Computing motif frequencies of the network"+str(networkf)+".")
        returned_motifs = network.motif.motif_freqs(networkf, degree, exclusive=True)
        for i in range(len(motifs)):
            motifs[i][1] = motifs[i][1] + returned_motifs[i][1]
    return motifs

__all__ =[motif_freqs, exclusive_motif_freqs]
        
    
    