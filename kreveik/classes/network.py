"""
Definition of network object.
"""

import numpy as num
import matplotlib.pyplot as plt
import copy
import itertools 
import logging
from kreveik.classes import *
import kreveik.probes as probes
from kreveik import *


class TopologicalNetwork(ProbeableObj):
    """
    This object is a stripped down network, designated to be a core 
    object for all network-like objects, like sub-graphs and motifs.
    """
    def __init__ (self,adjacency_matrix):
        ProbeableObj.__init__(self)
        self.adjacency = num.array(adjacency_matrix,dtype=bool)
        self.code = str(len(self.adjacency))+"-"+str(reduce(lambda x,y : 2*x+y, 
                                                              self.adjacency.flatten()*1))
    
    def indegree(self):
        return self.adjacency.sum(axis=0)
    
    def outdegree(self):
        return self.adjacency.sum(axis=1)
    
    def graph(self):
        """Returns a pydot graph object.    
        """
        import pydot
        
        node_orig = 1
    
        graph = pydot.Dot(graph_type='digraph')

        for row in self.adjacency:
            skip = 0
            r = row
            node_dest = skip+1
    
            for e in r:
                if e:
                    graph.add_edge(
                        pydot.Edge( node_orig, node_dest) )
                node_dest += 1
            node_orig += 1
    
        return graph

        
        
    def is_connected(self):
        """
        Returns True if the graph is connected, False if not.
        uses the algorithm explained in 
        http://keithbriggs.info/documents/graph-eigenvalues.pdf
        """
        symmetric = self.adjacency+self.adjacency.T-num.diag(
                                 self.adjacency.diagonal())
        if (0 in symmetric.sum(axis=0) or 0 in symmetric.sum(axis=1)):
            return False
        degrees = num.diagflat(symmetric.sum(axis=0))
        laplacian = degrees-symmetric
        determinant = num.linalg.det(laplacian +num.ones((len(laplacian),len(laplacian) )))
        return not(determinant == 0)
    
    def copy(self):
        """
        Returns a copy of the Topological Network object. 
        """
        return copy.deepcopy(self)
    
    def save(self,filename):
        """
        Saves the Network as an object to a file specified.
        """
        import pickle
        try:
            filehandler = open(filename+".net", 'w')
            pickle.dump(self,filehandler) 
        except pickle.PickleError:
            logging.error("The object failed to be pickled.")

            

class Motif(TopologicalNetwork):
    """
    Motif is a 
    """
    def __init__(self, adjacency_matrix):
        TopologicalNetwork.__init__(self, adjacency_matrix)
        self.degree = len(adjacency_matrix)
    
    def __eq__(self,other):
        permutation_list = itertools.permutations(range(self.degree),self.degree)
        for permutation in permutation_list:
            
            if num.sum(self.indegree()) != num.sum(other.indegree()):
                return False

            newarray = num.zeros((len(self.adjacency),len(self.adjacency)),dtype=bool)
            #newarray[[node_init,node_end]] = newarray[[node_end,node_init]]
            #newarray[:,[node_init,node_end]] = newarray[:,[node_end,node_init]]
            for rowctr,row in enumerate(self.adjacency):
                for colctr,col in enumerate(row):
                    if col == True:
                        newarray[permutation[rowctr]][permutation[colctr]]= True
        
            if num.all(newarray == other.adjacency):
                return True
            
        return False    


class Network(TopologicalNetwork,Element):
    '''
    Network Class
    
    Input Arguments
        adjacency_matrix
        mask
        state_vec  
    '''
    def __init__ (self,adjacency_matrix,mask,function,state_vec=None):
        Element.__init__(self)
        TopologicalNetwork.__init__(self,adjacency_matrix)
        self.n_nodes= num.size(adjacency_matrix,0)
        self.mask=mask
        if state_vec == None:
            state_vec= (num.random.random((1,self.n_nodes))< 0.5)
        self.state=num.array(state_vec)
        self.function = function
    
    def __str__(self):
        return str(id(self))
        
    def info(self):
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
        
    def __getitem__(self, index):
        """
        nth item of a network object is the state that it is in, in the nth 
        iteration
        """
        if index > len(self.state):
            raise IndexError
        return self.state[index]
    
    def __contains__(self, state):
        """
        Returns a boolean according to whether a network includes the state  
        """
        item = num.array(state*True)
        return item in self.state
            
    def __call__ (self,state):
        """
        When a  network is called as a function, it sets the initial condition 
        as the given vector, finds the equilibrium of that state.
        """
        self.set_state(state)
        self.search_equilibrium(2**self.n_nodes,state,orbit_extraction=False,def_advance=1)
        
        
    def advance(self,times,start_from=None,*args):
        '''
        Advances the state in the phase space a given number of times.
        If a starter state is given, the initial condition is taken as the given state.
        If not, the last state is used instead.
        Input Arguments
            times -> the number of iterations to be taken.
            starter_state -> the initial state to be used
        '''
        
        if start_from != None:
            self.set_set(start_from)
        
        for counter in xrange(times):
            newstate = self.function(self,self.state[-1])
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
        """Creates a plot of the equilibria for all possible initial conditions
        in the phase space. Every point in the phase space corresponds to the 
        length of the orbit that initial condition is attracted to.
        """
        rowsandcols = 2**(len(self.adjacency)/2)
        if self.n_nodes % 2 == 0:
            im_matrix = self.equilibria.reshape((rowsandcols,rowsandcols))
        
        if self.n_nodes % 2 == 1:
            im_matrix = self.equilibria.reshape((rowsandcols,rowsandcols*2))
    
        plt.imshow(im_matrix,cmap=plt.cm.gray,interpolation='nearest')
        
        plt.grid()
        plt.colorbar()
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
        self.populate_probes(probes.populate_equilibria)

    

