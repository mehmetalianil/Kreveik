
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
scorers module
===============

This module contains different scorer functions that have a 
single network as input and outputs its score accordingly.

Functions
---------
    sum_scorer_f:
    orbit_length_sum_f
 
"""


 
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
    
    import numpy as num
    
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

