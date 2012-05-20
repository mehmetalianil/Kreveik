
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

import numpy as num
import kreveik
import logging

def random(n_nodes,function,probability=(0.5,0.5,0.5),connected=False):
    '''
    Generates and returns a random network with a random initial conditions.
    The adjacency matrix, initial state, boolean function are populated with 
    1's and 0's with probabilities of 0.5.
    
    Input Variables
    n_nodes -> Number of nodes in the system. A value of 2 to 8 will generate a 
    network with manageable size and complexity.
    probability -> The probability of having a connection in any two nodes. 
    A smaller value will decrease complexity and clustering coefficient.  
    scorer -> a function for the type network
    '''

    num.random.seed()
    adjacency_matrix=(num.random.random((n_nodes,n_nodes))<probability[0])
    state=(num.random.random((1,n_nodes))<probability[1])
    bool_fcn=(num.random.random((n_nodes,n_nodes))<probability[2])
    new_network = kreveik.classes.Network(adjacency_matrix, bool_fcn, function, state_vec=state)
    
    if connected==False:
        try:
            logging.info("Generating one network of node count "+str(n_nodes))
            return new_network
        
        except ValueError,e:
            z = e
            logging.error("Network is too big to model.")
            print z
            
    elif new_network.is_connected():
        try:
            logging.info("Generating one network of node count "+str(n_nodes))
            return new_network
        
        except ValueError,e:
            z = e
            logging.error("Network is too big to model.")
            print z
    else:
        while not new_network.is_connected():
            num.random.seed()
            adjacency_matrix=(num.random.random((n_nodes,n_nodes))<probability[0])
            state=(num.random.random((1,n_nodes))<probability[1])
            bool_fcn=(num.random.random((n_nodes,n_nodes))<probability[2])
            new_network = kreveik.classes.Network(adjacency_matrix, bool_fcn, function,state_vec=state)
        
        try:
            logging.info("Generating one network of node count "+str(n_nodes))
            return new_network
        except ValueError,e:
            z = e
            logging.error("Network is too big to model.")
            print z
         
    return new_network