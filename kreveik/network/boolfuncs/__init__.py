"""
For a network, every single node is taken, its mask and state vector is clipped.
They are subject to a boolean operation from numpy libraries.
Then from the fact that whether the node outputs a number greater than the 
shortened state vector, the node outputs 1 or 0.
These values are gathered up and outputted as a new state vector.
The method can be:
    num.logical_or
    num.logical_and
    num.logical_xor
    num.logical_xnor
    
    or any other function that outputs an integer with an input of two ndarrays.        
"""

from boolfuncs import *



