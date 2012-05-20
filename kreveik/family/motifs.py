
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


def motif_freqs(family,degree, sorting=False, **kwargs):
    """
    Returns a list of motifs of the family.
    """
    from kreveik import network
    import copy
    import logging
    
    if  'motiflist' in kwargs:
        returned_motifs = copy.deepcopy(kwargs['motiflist'])
    else:
        returned_motifs = network.motif.all_conn_motifs(degree)[:]

    logging.info("Computing motif frequencies of the family")
    for networkf in family:
        returned_motifs = network.motif.motif_freqs(networkf, degree, motiflist=returned_motifs)           
        
    if sorting:
        return  sorted (returned_motifs, key = lambda returned_motifs:returned_motifs[1] , reverse = True)
    else:
        return returned_motifs