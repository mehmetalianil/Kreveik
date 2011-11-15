"""
Definition of network object.
"""

from baseclasses import *
import numpy as num
import matplotlib.pyplot as plt
import copy
import networkx as nx
from ..probes import *
import itertools 

print_enable=True
debug = False

class TopologicalNetwork(ProbeableObj):
    """
    This object is a stripped down network, designated to be a core 
    object for all network-like objects, like sub-graphs and motifs.
    """
    def __init__ (self,adjacency_matrix):
        ProbeableObj.__init__(self)
        self.adjacency = adjacency_matrix
        
    def is_connected(self):
        """
        Returns True if the graph is connected, False if not.
        uses the algorithm explained in 
        http://keithbriggs.info/documents/graph-eigenvalues.pdf
        """
        if (0 in self.adjacency.sum(axis=0) or 0 in self.adjacency.sum(axis=1)):
            return False
        symmetric = self.adjacency+self.adjacency.T-num.diag(
                                 self.adjacency.diagonal())
        degrees = symmetric.sum(axis=0)
        laplacian = degrees-symmetric
        determinant = num.linalg.det(num.ones((len(laplacian),len(laplacian) )))
        return not(determinant == 0)
    
    def copy(self):
        """
        Returns a copy of the Topological Network object. 
        """
        return copy.copy(self)
    
    def save(self,filename):
        """
        Saves the Network as an object to a file specified.
        """
        import pickle
        try:
            filehandler = open(filename+".net", 'w')
            pickle.dump(self,filehandler) 
        except pickle.PickleError:
            print "The object failed to be pickled."
            
            
    def motif_freqs (self,degree):
        """
        Returns a list of motifs.
        """
    
        all_combinations = itertools.combinations(range(len(self.adjacency)),degree)
        motif_list = []
        
        for combination in all_combinations:
            if debug: 
                print "Motif Permutation:"+str(list(combination))
            
            this_motif_adj = num.zeros((degree,degree))
            for (first_ctr,first_node) in enumerate(list(combination)):
                for (second_ctr,second_node) in enumerate(list(combination)):
                    this_motif_adj[first_ctr][second_ctr] = self.adjacency[first_node][second_node]
            
            this_motif = Motif(this_motif_adj)

            if this_motif.is_connected():                
                truth = [this_motif == old_motif[0] for old_motif in motif_list]
                if (any(truth) == True):
                    index = truth.index(True)
                    motif_list[index][1] = motif_list[index][1]+1
                elif (all(truth) == False) or (len(truth)==0):
                    motif_list.append((this_motif,1))
                else:
                    print "There has been a problem while extracting Motifs"
                    break
            
        return motif_list

class Motif(TopologicalNetwork):
    """
    Motif
    """
    def __init__(self, adjacency_matrix):
        TopologicalNetwork.__init__(self, adjacency_matrix)
        self.degree = len(adjacency_matrix)
    
    def __eq__(self,other):
        permutation_list = itertools.permutations(range(self.degree),self.degree)
        for permutation in permutation_list:
            indegrees_match = [row_degree in other.adjacency.sum(axis=1) for 
                             row_degree in self.adjacency.sum(axis=1)]
            if not(all(indegrees_match)):
                return False
            outdegrees_match = [row_degree in other.adjacency.sum(axis=0) for 
                             row_degree in self.adjacency.sum(axis=0)]
            if not(all(outdegrees_match)):
                return False
            for (node_init,node_end) in enumerate(permutation):
                newarray = self.adjacency.copy()
                newarray[[node_init,node_end]] = newarray[[node_end,node_init]]
                newarray[:,[node_init,node_end]] = newarray[:,[node_end,node_init]]
            if num.all(newarray == other.adjacency):
                return True
        return False    


class Network(TopologicalNetwork):
    '''
    Network Class
    
    Input Arguments
        adjacency_matrix
        mask
        state_vec  
    '''
    def __init__ (self,adjacency_matrix,mask,score,function,state_vec=None):
        TopologicalNetwork.__init__(self,adjacency_matrix)
        self.n_nodes= num.size(adjacency_matrix,0)
        self.mask=mask
        if state_vec == None:
            state_vec= (num.random.random((1,self.n_nodes))< 0.5)
        self.state=num.array(state_vec)
        self.score = 0
        self.scorer = score
        self.function = function
    
    def print_id(self):
        '''
        Prints out an identification of the Network.
        Prints:
            Id
            Mothers
            Children
            Orbits
            Score
            Adjacency matrix
            sTate
            masK
        '''
        print "This network is : "+str(id(self))+"."
        print "Nodes: "+str(self.n_nodes)
        print "Score: "+str(self.score)
        print "Its mothers are: "
        print "   "+str(self.mother)
        print "Its children are: "
        for child in self.children:
            print "   "+str(child)
        print "It has the following adjacency matrix: "
        print self.adjacency
        print "The following are the masks for each node: "
        for (num,node) in enumerate(self.mask):
            print str(num)+" th node : "+str(node)
        print "The following are the states with respect to time "
        for (t,state) in enumerate(self.state):
            print "t= "+str(t)+" : "+str(node)
        print "The scorer is : "
        print self.scorer
            

    def advance(self,times,starter_state=None,*args):
        '''
        Advances the state in the phase space a given number of times.
        If a starter state is given, the initial condition is taken as the given state.
        If not, the last state is used instead.
        Input Arguments
            times -> the number of iterations to be taken.
            starter_state -> the initial state to be used
        '''
        
        
                     
        if starter_state == None:
            starter_state = self.state[-1]
        
        if "reset" in args:
            self.set_state(starter_state)
            
        
        for counter in xrange(times):
            newstate = self.function(self,starter_state)
            self.state = num.append(self.state,[newstate],axis=0)
            
        self.populate_probes(probes.advance)
        
    def set_state(self,state):
        """
        Flushes the state of the system, and sets the new state as the given one 
        """
        
        if type(state) == int:
            state = [int(strings)==True for strings in list(num.binary_repr(
                                                (state),width=self.n_nodes))]
        state_bool = [i == True for i in state]
        state = [list(state_bool)]
        self.state = num.array(state)
        
    def plot_state(self,last=20):
        '''
        Plots the last 20 states as a black and white strips vertically.
        The vertical axis is time, whereas each strip is a single state.
        Input Arguments
            last -> the number of states that will be plotted 
        '''
        # Take the state vector, convert the list of arrays into a 2d array, then show it as an image
        # Black and white. 
        
        plt.imshow(self.state[-last:],cmap=plt.cm.binary,interpolation='nearest')     
        plt.show()


    def plot_equilibria(self):
        
        # Take the state vector, convert the list of arrays into a 2d array, then show it as an image
        # Black and white. 
        
        # Future Modification 
        # May show a 'color' based on the whole state vector, easier for us to see states. 
        
        if self.n_nodes % 2 == 0:
            jumper = 2**(self.n_nodes/2)
            im_matrix = num.zeros((jumper,jumper))
            for ctr,offset in enumerate(num.multiply(range(jumper,jumper))):
                im_matrix[ctr,:] = self.equilibria[offset:jumper+offset]
        
        if self.n_nodes % 2 == 1:
            jumper = 2**(self.n_nodes/2+1)
            im_matrix = num.zeros((jumper/2,jumper))
            for ctr,offset in enumerate(num.multiply(range(jumper/2),jumper)):
                im_matrix[ctr,:] = self.equilibria[offset:jumper+offset]
    
        plt.imshow(im_matrix,cmap=plt.cm.gray,interpolation='nearest')
        
        plt.grid()
        plt.colorbar()
        plt.show()
        
    def hamming_distance(self,state_vector):
        '''
        Returns the Hamming distance of the specified vector to the state vectors that
        are available.
        Input Arguments:
            state_vector -> the vector that we'd like to calculate the Hamming distance to.
        '''
        return num.array(num.abs(state_vector-self.state)).sum(axis=1)
    
    def plot_hamming_distance(self,state_vector):
        '''
        Plots the Hamming distance of the specified vector to the state vectors that
        are available.
            state_vector -> the vector that we'd like to plot the Hamming distance to.
        '''
        plt.plot(self.hamming_distance_of_state(state_vector))
        plt.show()           
           
    def search_equilibrium(self,chaos_limit,starter_state,orbit_extraction=False,def_advance=1):
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
        if not(hasattr(self,"equilibria")):
            self.equilibria = num.zeros(2**self.n_nodes)
        if not(hasattr(self,"orbits")):
            if orbit_extraction:
                self.orbits = num.array([None]*2**self.n_nodes)
        
        self.set_state(starter_state)
        starter_state = self.state[-1]
        
        for ctr in xrange(chaos_limit):
            
            self.advance(def_advance)
            row = num.all(self.state[-1] == self.state, axis=1) 
            where = num.where(row==True)
            
            if len(where[0])> 1:
                frst_where = where[0][0]
                scnd_where = where[0][1]
                
                orbit_length = scnd_where-frst_where
                
                orbit = None
                location = reduce(lambda x,y : 2*x+y, starter_state)
                
                if orbit_extraction:
                    orbit = self.state[frst_where:scnd_where]
                    self.orbits[location] = orbit
                 
                self.equilibria[location] = orbit_length
                
                self.populate_probes(probes.search_equilibrium)
                return (orbit_length,orbit)
        
        
            
    def populate_equilibria(self,orbit_extraction=False):
        '''
        Creates all possible initial conditions by listing all possible 2^n boolean states.
        Then runs populate_equilibrium for each of them.
            populate_equilibrium returns orbits and-or degrees of the orbits.
        Gives scores to each of the networks, depending on the degree of the orbit each initial condition
        rests on.
        Input Arguments:
            normalize -> normalizes the scores to the value given.
        '''
  
        self.equilibria = num.zeros(2**self.n_nodes)
        if orbit_extraction:
            self.orbits = num.array([None]*2**self.n_nodes)
        
        binspace = range(0,num.power(2,self.n_nodes))
  
        for state in binspace:
            self.search_equilibrium(2**self.n_nodes,state,orbit_extraction)  
        
        self.score = self.scorer(self)
        self.populate_probes(probes.populate_equilibria)
        
    def degree(self):
        sum=[]
        for row in self.adjacency:
            sum.append(num.sum(row))
        return num.mean(sum)

    

