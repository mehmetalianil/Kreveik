"""
This module contains different scorer functions that have a 
single network as input and outputs its score accordingly.
"""

import numpy as num
 
def sum_scorer_f(network):
    """
    This function takes a network object and returns its score 
    computed by summing the lengths of orbits for every single 
    possible initial condition. If initial conditions turn 
    out to have the same attractors, they are counted again.
    """
    network.populate_equilibria()
    return sum(network.equilibria)/(2.0**(network.n_nodes))


def orbit_length_sum_f(network):
    """
    This function takes a network object and and returns its 
    score computed by summing the lengths of genuine orbits.
    """
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

