def motif_freqs(family,degree):
    """
    Returns a list of motifs of the family.
    """
    motif_list = []
    
    for (enum,network) in enumerate(family.network_list):
        all_combinations = itertools.combinations(range(len(network.adjacency)),degree)
        if verbose:
            print "Extracting motifs of Network #"+str(enum)+" of "+str(len(family.network_list))
        for combination in all_combinations:
        
            this_motif_adj = num.zeros((degree,degree))
            for (first_ctr,first_node) in enumerate(list(combination)):
                for (second_ctr,second_node) in enumerate(list(combination)):
                    this_motif_adj[first_ctr][second_ctr] = network.adjacency[first_node][second_node]
            
            this_motif = Motif(this_motif_adj)

            if this_motif.is_connected():                
                truth = [this_motif == old_motif for old_motif in motif_list]
                if (any(truth) == True):
                    index = truth.index(True)
                    motif_list[index].freq = motif_list[index].freq+1
                elif (all(truth) == False) or (len(truth)==0):
                    motif_list.append(this_motif)
                else:
                    print "There has been a problem while extracting Motifs"
                    break
            
    return motif_list