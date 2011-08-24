'''
Created on 09.02.2011

@author: Mehmet Ali Anil

The genereg package maintains class definitions and methods for manipulation,
statistical evaluation of random boolean networks. The emphasis is upon genetic
algorithm and how networks evolve accordingly.
'''

import numpy as num
import networkx as nx
import matplotlib.pyplot as plt
import genereg
import copy
import pickle
import sys

print_enable = False


__author__ = "Mehmet Ali Anil"
__copyright__ = ""
__credits__ = ["Mehmet Ali Anil"]
__license__ = "GPL"
__version__ = "0.0.5"
__maintainer__ = "Mehmet Ali Anil"
__email__ = "anilm@itu.edu.tr"
__status__ = "Production"
        

def generate_random(n_nodes,probability=(0.5,0.5,0.5)):
    '''
    Generates and returns a random network with a random initial conditions.
    The adjacency matrix, initial state, boolean function are populated with 
    1's and 0's with probabilities of 0.5.
    
    Input Variables
    n_nodes -> Number of nodes in the system. A value of 2 to 8 will generate a 
    network with manageable size and complexity.
    probability -> The probability of having a connection in any two nodes. 
    A smaller value will decrease complexity and clustering coefficient.  
    '''
    num.random.seed()
    adjacency_matrix=(num.random.random((n_nodes,n_nodes))<probability[0])*1.0
    #    First state of the system is determined
    state=(num.random.random((1,n_nodes))<probability[1])*1.0
    bool_fcn=(num.random.random((n_nodes,n_nodes))<probability[2])*1.0
    
    if print_enable:
        print adjacency_matrix
        print state
        print bool_fcn
    try:
        network(adjacency_matrix, bool_fcn, state)
    except ValueError,e:
        z = e
        print "Network is too big to model."
        print z
    
    return 

class family(object):
    '''
    Family Class.
    A class that will have a single family of networks, a genetic algorithm 
    will be run within a family. The macro parameters of a group of network, 
    though may also be reached from a list of networks, will be housed in a 
    family in a more structured manner.
    '''
    
    def __init__ (self,scorer):
        self.network_list = []
        self.wildtype_list = [] 
        self.equilibria = []
        self.scorer = scorer
    
    def add_to_family(self, network):
        '''
        This method will add a network to the specified family.
        network -> The network that is to be appended to the family.
        '''
        
        if type(network) != genereg.network:
            print "The object that you're trying to append doesn't seem to be a network"
            print "Please double check."
            return False
        
        if network in self.network_list:
            print "The network that you're trying to add to the family is already a member."
            print "Please clone the individual and append the clone."
            return False
        
        self.network_list.append(network)
        return True
            
    def plot_equilibria(self):
                   
        plt.plot(self.equilibria)
        
        # Wont go on unless the Window is closed.
        plt.colorbar()
        plt.show()
        
    def populate_wildtype(self,wildtype_threshold):
        '''
        Finds the wild types in a family and populates the list wildtype_list with them.
        Input Arguments
            wildtype_threshold -> a threshold for the score of he individual in order to attend
            the wildtype club.
        '''
        if len(self.equilibria) == 0:
            if print_enable:
                print "Warning: Equilibria not found."
                print "Populating equilibria ..."
            self.populate_equilibria_in_family()
            if print_enable:
                print "    Done!"
        
        print "Checking individuals in this family by their scores"
        for network in self.network_list:
            if network.score == 0:
                if print_enable:
                    print "Warning: Network "+str(network.id)+" has no information on its equilibrium"
                    print "Now calculating its equilibria..."
                network.populate_equilibria()
                if print_enable:    
                    print "    Done!"
                
            if network.score < wildtype_threshold:
                if print_enable:
                    print "Network "+str(network.id)+" is wild."
                self.wildtype_list.append(network)
    
        return True
    
    def populate_equilibria_in_family(self):
        '''
        If the family has individuals, it goes to each individual and finds the equilibria 
        for all possible initial conditions they may face. The orbits and scores are 
        assigned to each one of them.
        '''
        
        if len(self.network_list) == 0:
            print "Warning: There is nobody in this family."
            print "Please adopt individuals."
            return False
            
        self.equilibria = num.zeros(len(self.network_list))
        
        for id,network in enumerate(self.network_list): 
            if print_enable:
                print "Populating equilibrium for "+str(id)+", namely: "+str(network.id)
            network.populate_equilibria()
            self.equilibria[id] = network.score
            
    def genetic_iteration(self,score_threshold,mutant_recipe=('Both',1),howmany_gntc=1):
        '''
        Runs one iteration of the genetic algorithm.
        It finds wildtypes of the family, mutates them, populates the family with mutants
        and assasinates as much of it has mutated. 
        '''
        if self.wildtype_list != []:
            self.wildtype_list = []
        print "Determining wildtypes"
        self.populate_wildtype(score_threshold)
        print str(len(self.wildtype_list))+"wild individuals"
        kill_count = len(self.wildtype_list)
        family_count = len(self.network_list)
        
        #    Prepare a vector that has ones for each to be killed, zeroes for all remain.
        #    and permute its elements randomly.
        
        array = [1]*kill_count+[0]*(family_count-kill_count)
 
        random_kill_list = num.random.permutation(array)
        
        #    Tag each element as None for those who'll be killed
        
        for number,to_be_killed in enumerate(random_kill_list):
            if to_be_killed == 1:
                if print_enable:
                    print str(self.network_list[number].id)+" is killed with score"+str(self.network_list[number].score) 
                self.network_list[number] = None
                
        #    If there are ones that are killed, populate the remaining gaps with mutated wildtypes.
        counter_wt = 0
        
        for id,all_networks in enumerate(self.network_list):
            if all_networks == None:
                if print_enable:
                    print "mutating network "+str(self.wildtype_list[counter_wt].id)
                self.network_list[id] = self.wildtype_list[counter_wt].mutant(mutated_obj=mutant_recipe,howmany=howmany_gntc)[0]
                if print_enable:    
                    print "finding equilibria of the new network "+str(self.network_list[id].id)
                self.network_list[id].populate_equilibria()
                self.equilibria[id] = self.network_list[id].score
                counter_wt = counter_wt +1
                
        if all([type(i)==genereg.network for i in self.network_list])==True:
            print "New bunch created."
            return self.equilibria
        else:
            print "Unable to create new bunch"
            return False

    def genetic_algorithm(self,howmany=5):
        
        scores = []
        kout=[]
        self.populate_equilibria_in_family()
        
        for i in range(howmany):
            meanscore = self.equilibria.mean()
            petri1.genetic_iteration(18)
            scores.append(petri1.equilibria.tolist())
            all_degrees = [net.nx.in_degree().values() for net in petri1.network_list]
            kout.append(all_degrees)
            
class network(object):
    '''
    Network Class
    
    Input Arguments
        adjacency_matrix
        maskm
        state_vec  
    '''
    def __init__ (self,adjacency_matrix,mask,state_vec=None):
        self.id=id(self)
        self.adjacency=adjacency_matrix
        self.n_nodes= num.size(adjacency_matrix,0)
        self.mask=mask
        self.state=list()
        if state_vec == None:
            state_vec= num.zeros(self.n_nodes)
        self.state.append(state_vec)
        self.nx=nx.DiGraph(adjacency_matrix)
        self.equilibria=num.ones((num.power(2,self.n_nodes/2),num.power(2,self.n_nodes/2))).tolist()
        self.orbits = num.zeros((num.power(2,self.n_nodes/2),num.power(2,self.n_nodes/2))).tolist()
        self.score = 0
        self.mama = []
        self.children = []
        self.scorer = None
    
    def print_id(self,content='imcasatk'):
        '''
        Prints out an identification of the network.
        Prints:
            Id
            Mothers
            Children
            Orbits
            Resultant_equilibrium
            Score
            Adjacency matrix
            sTate
            masK
        '''
        pass
        
    def status(self):
        '''
        Prints out the initial status of the network, namely, the
            adjacency_matrix
            state
        '''
        print "State:"
        print self.state[-1]
        print "Adjacency Matrix:"
        print self.adjacency
        
        
    def show_graph(self,type='circular'):
        '''
        Visualizes the network with the help of networkx class generated from the
        adjacency matrix.
        '''
        if type is 'circular':
            nx.draw_circular(self.nx)
        if type is 'random':
            nx.draw_random(self.nx)
        if type is 'graphviz':
            nx.draw_graphviz(self.nx)
        if type is 'normal':
            nx.draw(self.nx,pos=nx.spring_layout(self.nx))
        plt.show()


    def advance(self,times,starter_state=None):
        '''
        Advances the state in the phase space a given number of times.
        If a starter state is given, the initial condition is taken as the given state.
        If not, the last state is used instead.
        Input Arguments
            times -> the number of iterations to be taken.
            starter_state -> the initial state to be used
        '''
                
        # it no initial state is given, the last state is the initial state.
        
        if starter_state == None:
            starter_state = self.state[-1]
        
        first_newstate=len(self.state)    
        self.state.extend(num.zeros((times,self.n_nodes))) 
        
        # advance n times
        
        for n in range(0,times):
        
        #    For all nodes in the graph,
            
            newstate=num.zeros(self.n_nodes)
            for i in range(0,self.n_nodes):
                
                #    Detect all nodes that have an incoming connection
                
                nonzero_of_adj = self.adjacency[i,].ravel().nonzero()[0]
                #    Reduce the boolean function and the state to a boolean function
                #     and state concerning only the incoming connections.
                
                short_mask = self.mask[i,].take(nonzero_of_adj)
                short_state = self.state[first_newstate-1+n].take(nonzero_of_adj)

                #    Two vectors are AND'ed element wise, and is summed in modulo 2
                #    This corresponds to i th node operating its boolean function over the same
                #    state vector.
                
                newstate[i]=num.int((len(short_state)/2) < (num.logical_xor(short_state,short_mask).sum()))
            self.state[n+first_newstate]=newstate
            
    def plot_state(self,last=20):
        '''
        Plots the last 20 states as a black and white strips vertically.
        The vertical axis is time, whereas each strip is a single state.
        Input Arguments
            last -> the number of states that will be plotted 
        '''
        # Take the state vector, convert the list of arrays into a 2d array, then show it as an image
        # Black and white. 
        
        # Future Modification 
        # May show a 'color' based on the whole state vector, easier for us to see states. 
        
        plt.imshow(num.array(self.state[-last:]),cmap=plt.cm.binary,interpolation='nearest')
        
        # Wont go on unless the Window is closed.
        
        plt.show()





    def plot_equilibria(self):
        
        # Take the state vector, convert the list of arrays into a 2d array, then show it as an image
        # Black and white. 
        
        # Future Modification 
        # May show a 'color' based on the whole state vector, easier for us to see states. 
        
        plt.imshow(self.equilibria,cmap=plt.cm.gray,interpolation='nearest')
        
        # Wont go on unless the Window is closed.
        plt.colorbar()
        plt.show()
        
    def hamming_distance_of_state(self,state_vector):
        '''
        Returns the Hamming distance of the specified vector to the state vectors that
        are available.
        Input Arguments:
            state_vector -> the vector that we'd like to calculate the Hamming distance to.
        '''
        return num.array(num.abs(state_vector-num.array(self.state))).sum(axis=1)
    
    def plot_hamming_distance_of_state(self,state_vector):
        '''
        Plots the Hamming distance of the specified vector to the state vectors that
        are available.
            state_vector -> the vector that we'd like to plot the Hamming distance to.
        '''
        plt.plot(self.hamming_distance_of_state(state_vector))
        plt.show()           
           
    def search_equilibrium(self,chaos_limit,starter_state,orbit_extraction=False):
        '''
        Searches for an equilibrium point, or a limit cycle. 
        Returns the state vector, or the state vector list, if the equilibrium is a limit cycle.
        If no equilibrium is found, returns False.
        Input Arguments:
            starter_state -> the initial state vector that the state will evolve on.
            chaos_limit -> the degree that an orbit will be considered as chaotic.
                The calculation will stop when this point is reached.
            orbit_extraction -> True when every individual orbit is recorded with its degree.
        '''
        
        #flushes states
        
        self.state = [num.array(starter_state)]
        
        #Advances chaos limit times.
        #self.advance(chaos_limit)
        
        # A memory of chaos limit is created, preallocation.
        
        #memory = num.zeros((chaos_limit,self.n_nodes))
        
        memory = num.array([[None]*self.n_nodes]*chaos_limit)
        
        # to the first memory block, the initial state is written. 
        
        memory_ctr = 0
        
        while (memory_ctr < chaos_limit):
            
            memory [memory_ctr] = self.state[-1]
            #advance once , last state will be a new one 

            self.advance(1,starter_state)
            
            # VERY INEFFICIENT EXTREMELY EXTRAVAGANT!!!
            # BUT WORKS.
            # We'd like to remove tolist s
            
            
            # All matrices are converted into lists.
            memory_as_list = memory.tolist()
            last_state_as_list = num.array(self.state).tolist()[-1]
            
            # if this particular state we are concerned with is present in the memory 
            if last_state_as_list in memory_as_list:
                # Where in the memory is this particular state?
                where = memory_as_list.index(last_state_as_list)
                # If We'd like to extract the orbit out, for all states in the memory, 
                for state in memory[0:where]:
                    # Convert the state to a list
                    state_as_list = state.tolist()
                    # These are only necessary for the matrix representation.
                    first_half_of_state = state[:len(state_as_list)/2]
                    second_half_of_state = state[len(state_as_list)/2:]
                    # Finds the decimal representation of the binary number
                    first_location_in_equilibrium = int(reduce(lambda s, x: s*2 + x, first_half_of_state))
                    second_location_in_equilibrium = int(reduce(lambda s, x: s*2 + x, second_half_of_state))
                    # Memory_ctr is the present number of iteration, whereas Where is the last identical state
                    self.equilibria[first_location_in_equilibrium][second_location_in_equilibrium] = memory_ctr-where+1
                    # Extract orbits, if it was requested to do so.
                    if orbit_extraction == True:
                        self.orbits[first_location_in_equilibrium][second_location_in_equilibrium] = memory [:memory_ctr]
                return (memory [:memory_ctr+1],memory_ctr-where+1)
            memory_ctr += 1
            
    def populate_equilibria(self,normalize=1):
        '''
        Creates all possible initial conditions by listing all possible 2^n boolean states.
        Then runs populate_equilibrium for each of them.
            populate_equilibrium returns orbits and-or degrees of the orbits.
        Gives scores to each of the networks, depending on the degree of the orbit each initial condition
        rests on.
        Input Arguments:
            normalize -> normalizes the scores to the value given.
        '''
 
        # Creates all possible initial conditions by listing all possible integers from 0 to 2^n_node-1
        # Converts them all to binaries, fills them all with zeroes such that they are all in the
        # form of 000111010 rather than 111010. Then creates a list out of them.
        
        state_numbers_decimal = range(0,num.power(2,self.n_nodes))
        binspace = [list((bin(k)[2:].zfill(self.n_nodes))) for k in state_numbers_decimal]
        
        # But this list has elements of strings. We convert all of the elements to integers
        
        int_binspace=[[int(i) for i in k] for k in binspace] 
        
        for state in int_binspace:
            self.search_equilibrium(100,state)  
        
        self.score = self.scorer()
        
    def mutant(self, mutated_obj=('Both',1), rule=None, howmany=1):
        '''
        Will result in mutation
        Returns mutated network.
        
        Arranges the identification of the newcomer.
        Input Arguments:
            mutated_obj -> A tuple is fed, the first argument of the tuple determines the nature of the 
            mutation, whereas the second argument determines number of mutations inflicted on each round.
            rule -> If possible, a rule for mutation will be implemented.
            howmany -> The number of mutants that will be returned for each call. 
        '''
        
        mutant_list = []
        
        for mutant_ctr in range(0,howmany):
            
            mutated_network = copy.copy(self)
            mutant_adj = copy.copy(mutated_network.adjacency)
            mutant_mask = copy.copy(mutated_network.mask)
            
            if (mutated_obj[0] == 'Both' or mutated_obj[0] == 'Connections'):
                num.random.seed()
                random_i = num.random.randint(0, self.n_nodes-1, size=mutated_obj[1])
                num.random.seed()
                random_j = num.random.randint(0, self.n_nodes-1, size=mutated_obj[1])
                for ith_row in random_i:
                    for jth_column in random_j:
                        if mutant_adj[ith_row][jth_column] == 1:
                            mutant_adj[ith_row][jth_column] = 0
                        elif mutant_adj[ith_row][jth_column] == 0:
                            mutant_adj[ith_row][jth_column] = 1
                        
            
            if (mutated_obj[0] == 'Both' or mutated_obj[0] == 'Mask'):
                num.random.seed()
                random_i = num.random.randint(0, self.n_nodes-1, size=mutated_obj[1])
                num.random.seed()
                random_j = num.random.randint(0, self.n_nodes-1, size=mutated_obj[1])
                for ith_row in random_i:
                    for jth_column in random_j:
                        if mutant_mask[ith_row][jth_column] == 1:
                            mutant_mask[ith_row][jth_column] = 0
                        elif mutant_mask[ith_row][jth_column] == 0:
                            mutant_mask[ith_row][jth_column] = 1
                        
            mutated_network.adjacency = mutant_adj
            mutated_network.mask = mutant_mask
            
            ##
            # Records the fact that self is the mama of the mutant.
            # Has no children, et cetera.
            
            mutated_network.mama = copy.copy(self.mama)
            mutated_network.mama.append(id(self))
            mutated_network.id = id(mutated_network)
            mutated_network.children = []
            mutated_network.nx=nx.DiGraph(mutated_network.adjacency)
            
            ##
            # Records that self has a mutant child somewhere
            
            self.children.append(mutated_network.id)
            mutant_list.append(mutated_network) 
            
        return mutant_list
    
def sum_scorer(family):
    return sum([sum(k) for k in family.equilibria])
    
   