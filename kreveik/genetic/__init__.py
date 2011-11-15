verbose=True
from ..probes import *
import wildtype

def populate_wildtype(family,wildtype_check):
    '''
    Finds the wild types in a family and populates the list wildtype_list with them.
    Input Arguments
        wildtype_threshold -> a threshold for the score of he individual in order to attend
        the wildtype club.
    '''
    
    if len(family.scores) == 0:
        if verbose:
            print "Warning: Equilibria not found."
            print "Populating equilibria ..."
        family.populate_equilibria_in_family()
        if verbose:
            print "    Done!"
    
    print "Checking individuals in this family by their scores"
    for network in family.network_list:
        if network.score == 0:
            if verbose:
                print "Warning: Network "+str(network)+" has no information on its equilibrium"
                print "Now calculating its equilibria..."
            network.populate_equilibria()
            if verbose:    
                print "    Done!"
            
        if wildtype_check(network) :
            if verbose:
                print "Network "+str(id(network))+" is wild."
            family.wildtype_list.append(network)
    
    family.populate_probes(probes.populate_wildtype)
    return True

def genetic_iteration(family):
    '''
    Runs one iteration of the genetic algorithm.
    It finds wildtypes of the family, mutates them, populates the family with mutants
    and assasinates as much of it has mutated. 
    '''
    if family.wildtype_list != []:
        family.wildtype_list = []
    if verbose:
        print "Determining wildtypes"
    family.populate_wildtype(score_threshold)
    if verbose:
        print str(len(family.wildtype_list))+"wild individuals"
    kill_count = len(family.wildtype_list)
    family_count = len(family.network_list)
    
    #    Prepare a vector that has ones for each to be killed, zeroes for all remain.
    #    and permute its elements randomly.
    
    array = [1]*kill_count+[0]*(family_count-kill_count)

    random_kill_list = num.random.permutation(array)
    
    #    Tag each element as None for those who'll be killed
    
    for number,to_be_killed in enumerate(random_kill_list):
        if to_be_killed == 1:
            if verbose:
                print str(family.network_list[number])+" is killed with score"
                +str(family.network_list[number].score) 
            family.network_list[number] = None
            
    #    If there are ones that are killed, populate the remaining gaps with mutated wildtypes.
    counter_wt = 0
    
    for network_ctr,all_networks in enumerate(family.network_list):
        if all_networks == None:
            if verbose:
                print "mutating network "+str(family.wildtype_list[counter_wt])
                
            family.network_list[network_ctr] = family.wildtype_list[counter_wt].mutant(mutated_obj
                                                        =mutant_recipe,howmany=howmany_gntc)[0]
                                                        
            if verbose:    
                print "finding equilibria of the new network "+str(family.network_list[network_ctr])
            family.network_list[network_ctr].populate_equilibria()
            family.scores[network_ctr] = family.network_list[network_ctr].score
            counter_wt = counter_wt +1
            
    family.scores_history = num.append(family.scores_history,family.scores)
    family.populate_probes(probes.genetic_iteration)
    return family.scores

def genetic_algorithm(family,howmany=5,*args,**kwargs):
    """
    The wrapper for consecutive genetic iterations.
    """
    family.populate_equilibria_in_family()
    
    for ctr in range(howmany[0]):
        meanscore = family.scores.mean()
        if verbose:
            print "Iteration "+str(ctr)+" Mean Score is: "+str(meanscore)
        family.genetic_iteration(meanscore,howmany[1])
    family.populate_probes(probes.genetic_algorithm)

