"""
This module contains different scorers that have a 
single network as input and outputs its score accordingly.
"""
print_enable = True
import numpy as num

def sum_scorer(network):
    # The worst case is an orbit that walks the whole state space.
    # Thus the scores are normalized to that value.
    return sum(network.equilibria)/(2.0**(2*network.n_nodes))

def orbit_length_sum(network):
    binspace = range(0,num.power(2,network.n_nodes))
    genuine_orbits = []
    genuine_orbit_lengths=[]
    for state in binspace:
        (orbit_length,orbit) = network.search_equilibrium(2**network.n_nodes,state,True)
        is_in_list = False
        for old_orbit in genuine_orbits:
            for state in old_orbit:
                if all(state == orbit[-1]):
                    is_in_list = True
        if is_in_list == False:
            genuine_orbits.append(orbit)
            genuine_orbit_lengths.append(orbit_length)
    return sum(genuine_orbit_lengths)
